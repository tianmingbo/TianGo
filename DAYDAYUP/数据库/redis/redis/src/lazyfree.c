#include "server.h"
#include "bio.h"
#include "atomicvar.h"
#include "cluster.h"

static size_t lazyfree_objects = 0;
pthread_mutex_t lazyfree_objects_mutex = PTHREAD_MUTEX_INITIALIZER;

/* Return the number of currently pending objects to free. */
size_t lazyfreeGetPendingObjectsCount(void) {
    size_t aux;
    atomicGet(lazyfree_objects, aux);
    return aux;
}

/*
 * 什么情况才会真正异步释放内存？这和 key 的类型、编码方式、元素数量都有关系（详见 lazyfreeGetFreeEffort 函数）：
 * a) 当 Hash/Set 底层采用哈希表存储（非 ziplist/int 编码存储）时，并且元素数量超过 64 个
 * b) 当 ZSet 底层采用跳表存储（非 ziplist 编码存储）时，并且元素数量超过 64 个
 * c) 当 List 链表节点数量超过 64 个（注意，不是元素数量，而是链表节点的数量，List 底层实现是一个链表，链表每个节点是一个 ziplist，一个 ziplist 可能有多个元素数据）
 * 只有满足以上条件，在释放 key 内存时，才会真正放到「后台线程」中执行，其它情况一律还是在主线程操作。
 * 也就是说 String（不管内存占用多大）、List（少量元素）、Set（int 编码存储）、Hash/ZSet（ziplist 编码存储）这些情况下的 key，在释放内存时，依旧在「主线程」中操作。
 *
 * 可见，即使打开了 lazy-free，String 类型的 bigkey，在删除时依旧有「阻塞」主线程的风险。所以，即便 Redis 提供了 lazy-free，还是不建议在 Redis 存储 bigkey
 *
 * Redis 在释放内存「评估」代价时，不是看 key 的内存大小，而是关注释放内存时的「工作量」有多大。
 * 从上面分析可以看出，如果 key 内存是连续的，释放内存的代价就比较低，则依旧放在「主线程」处理。
 * 如果 key 内存不连续（包含大量指针），这个代价就比较高，这才会放在「后台线程」中执行
 * */
size_t lazyfreeGetFreeEffort(robj *obj) {
    if (obj->type == OBJ_LIST) {
        quicklist *ql = obj->ptr;
        return ql->len;
    } else if (obj->type == OBJ_SET && obj->encoding == OBJ_ENCODING_HT) {
        dict *ht = obj->ptr;
        return dictSize(ht);
    } else if (obj->type == OBJ_ZSET && obj->encoding == OBJ_ENCODING_SKIPLIST) {
        zset *zs = obj->ptr;
        return zs->zsl->length;
    } else if (obj->type == OBJ_HASH && obj->encoding == OBJ_ENCODING_HT) {
        dict *ht = obj->ptr;
        return dictSize(ht);
    } else if (obj->type == OBJ_STREAM) {
        size_t effort = 0;
        stream *s = obj->ptr;

        /* Make a best effort estimate to maintain constant runtime. Every macro
         * node in the Stream is one allocation. */
        effort += s->rax->numnodes;

        /* Every consumer group is an allocation and so are the entries in its
         * PEL. We use size of the first group's PEL as an estimate for all
         * others. */
        if (s->cgroups) {
            raxIterator ri;
            streamCG *cg;
            raxStart(&ri, s->cgroups);
            raxSeek(&ri, "^", NULL, 0);
            /* There must be at least one group so the following should always
             * work. */
            serverAssert(raxNext(&ri));
            cg = ri.data;
            effort += raxSize(s->cgroups) * (1 + raxSize(cg->pel));
            raxStop(&ri);
        }
        return effort;
    } else {
        return 1; /* Everything else is a single allocation. */
    }
}

/* Delete a key, value, and associated expiration entry if any, from the DB.
 * If there are enough allocations to free the value object may be put into
 * a lazy free list instead of being freed synchronously. The lazy free list
 * will be reclaimed in a different bio.c thread. */
#define LAZYFREE_THRESHOLD 64

// 非阻塞删除逻辑
int dbAsyncDelete(redisDb *db, robj *key) {
    /* 如果过期字典中存在该键,则先从过期字典中删除该键 */
    if (dictSize(db->expires) > 0) dictDelete(db->expires, key->ptr);

    /* 将该键从数据库字典中删除,返回键值对,这时并没有删除键值对对象 */
    dictEntry *de = dictUnlink(db->dict, key->ptr);
    if (de) {
        robj *val = dictGetVal(de);
        // 评估「代价」，如果代价很小，那么就直接在「主线程」操作了
        size_t free_effort = lazyfreeGetFreeEffort(val);

        /* 如果值对象占用的字节数大于LAZYFREE_THRESHOLD,
         * 并且该值的引用计数为1,则执行非阻塞删除 */
        if (free_effort > LAZYFREE_THRESHOLD && val->refcount == 1) {
            atomicIncr(lazyfree_objects, 1);
            // 创建一个后台任务负责删除值对象
            bioCreateBackgroundJob(BIO_LAZY_FREE, val, NULL, NULL);
            // 将该键值对的值对象引用设置为NULL,保证主线程无法再访问该值对象
            dictSetVal(db->dict, de, NULL);
        }
    }

    /* 删除键值对对象,并释放内存空间.
     * 如果是非阻塞删除,那么这里值对象引用已经被设置为NULL,并不会阻塞当前线程 */
    if (de) {
        dictFreeUnlinkedEntry(db->dict, de);
        if (server.cluster_enabled) slotToKeyDel(key);
        return 1;
    } else {
        return 0;
    }
}

/* Free an object, if the object is huge enough, free it in async way. */
void freeObjAsync(robj *o) {
    size_t free_effort = lazyfreeGetFreeEffort(o);
    if (free_effort > LAZYFREE_THRESHOLD && o->refcount == 1) {
        atomicIncr(lazyfree_objects, 1);
        bioCreateBackgroundJob(BIO_LAZY_FREE, o, NULL, NULL);
    } else {
        decrRefCount(o);
    }
}

/* Empty a Redis DB asynchronously. What the function does actually is to
 * create a new empty set of hash tables and scheduling the old ones for
 * lazy freeing. */
void emptyDbAsync(redisDb *db) {
    dict *oldht1 = db->dict, *oldht2 = db->expires;
    db->dict = dictCreate(&dbDictType, NULL);
    db->expires = dictCreate(&keyptrDictType, NULL);
    atomicIncr(lazyfree_objects, dictSize(oldht1));
    bioCreateBackgroundJob(BIO_LAZY_FREE, NULL, oldht1, oldht2);
}

/* Empty the slots-keys map of Redis CLuster by creating a new empty one
 * and scheduiling the old for lazy freeing. */
void slotToKeyFlushAsync(void) {
    rax *old = server.cluster->slots_to_keys;

    server.cluster->slots_to_keys = raxNew();
    memset(server.cluster->slots_keys_count, 0,
           sizeof(server.cluster->slots_keys_count));
    atomicIncr(lazyfree_objects, old->numele);
    bioCreateBackgroundJob(BIO_LAZY_FREE, NULL, NULL, old);
}

/* Release objects from the lazyfree thread. It's just decrRefCount()
 * updating the count of objects to release. */
void lazyfreeFreeObjectFromBioThread(robj *o) {
    decrRefCount(o);
    atomicDecr(lazyfree_objects, 1);
}

/* Release a database from the lazyfree thread. The 'db' pointer is the
 * database which was substitutied with a fresh one in the main thread
 * when the database was logically deleted. 'sl' is a skiplist used by
 * Redis Cluster in order to take the hash slots -> keys mapping. This
 * may be NULL if Redis Cluster is disabled. */
void lazyfreeFreeDatabaseFromBioThread(dict *ht1, dict *ht2) {
    size_t numkeys = dictSize(ht1);
    dictRelease(ht1);
    dictRelease(ht2);
    atomicDecr(lazyfree_objects, numkeys);
}

/* Release the skiplist mapping Redis Cluster keys to slots in the
 * lazyfree thread. */
void lazyfreeFreeSlotsMapFromBioThread(rax *rt) {
    size_t len = rt->numele;
    raxFree(rt);
    atomicDecr(lazyfree_objects, len);
}
