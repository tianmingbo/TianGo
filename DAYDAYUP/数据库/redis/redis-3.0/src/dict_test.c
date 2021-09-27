#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <limits.h>
#define DICT_OK 0
#define DICT_ERR 1

// 比对两个键
#define dictCompareKeys(d, key1, key2) \
    (((d)->type->keyCompare) ? (d)->type->keyCompare((d)->privdata, key1, key2) : (key1) == (key2))
// 设置给定字典节点的键
#define dictSetKey(d, entry, _key_)                               \
    do                                                            \
    {                                                             \
        if ((d)->type->keyDup)                                    \
            entry->key = (d)->type->keyDup((d)->privdata, _key_); \
        else                                                      \
            entry->key = (_key_);                                 \
    } while (0)

#define dictFreeVal(d, entry)     \
    if ((d)->type->valDestructor) \
    (d)->type->valDestructor((d)->privdata, (entry)->v.val)

// 设置给定字典节点的值
#define dictSetVal(d, entry, _val_)                                 \
    do                                                              \
    {                                                               \
        if ((d)->type->valDup)                                      \
            entry->v.val = (d)->type->valDup((d)->privdata, _val_); \
        else                                                        \
            entry->v.val = (_val_);                                 \
    } while (0)

#define dictIsRehashing(ht) ((ht)->rehashidx != -1)
#define dictHashKey(d, key) (d)->type->hashFunction(key)
#define dictGetVal(he) ((he)->v.val)
#define DICT_HT_INITIAL_SIZE 4
#define dictSize(d) ((d)->ht[0].used + (d)->ht[1].used)
static int dict_can_resize = 1;
static unsigned int dict_force_resize_ratio = 5;

typedef struct dictEntry
{
    void *key;
    union
    {
        void *val;
        uint64_t u64;
        int64_t s64;
    } v;
    //执行下一个哈希表节点
    struct dictEntry *next;
} dictEntry;

typedef struct dictht
{
    dictEntry **table;
    unsigned long size;
    unsigned long sizemask;
    unsigned long used;
} dictht;

/*
 * 字典类型特定函数
 */
typedef struct dictType
{

    // 计算哈希值的函数
    unsigned int (*hashFunction)(const void *key);

    // 复制键的函数
    void *(*keyDup)(void *privdata, const void *key);

    // 复制值的函数
    void *(*valDup)(void *privdata, const void *obj);

    // 对比键的函数
    int (*keyCompare)(void *privdata, const void *key1, const void *key2);

    // 销毁键的函数
    void (*keyDestructor)(void *privdata, void *key);

    // 销毁值的函数
    void (*valDestructor)(void *privdata, void *obj);

} dictType;

typedef struct dict
{
    dictType *type;
    void *privdata;
    dictht ht[2];
    int rehashidx;
    int iterators;
} dict;

static void _dictReset(dictht *ht)
{
    ht->table = NULL;
    ht->size = 0;
    ht->sizemask = 0;
    ht->used = 0;
}

int _dictInit(dict *d, dictType *type, void *privDataPtr)
{
    _dictReset(&d->ht[0]);
    _dictReset(&d->ht[1]);

    d->type = type;
    d->privdata = privDataPtr;
    d->rehashidx = -1;
    d->iterators = 0;
    return DICT_OK;
}

dict *diceCreate(dictType *type, void *privDataPtr)
{
    dict *d = malloc(sizeof(*d));
    _dictInit(d, type, privDataPtr);
    return d;
}

int dictRehash(dict *d, int n)
{
    if (!dicytIsRehashing(d))
        return 0;
    while (n--)
    {
        dictEntry *de, *nextde;
        if (d->ht[0].used == 0)
        {
            free(d->ht[0].table);
            d->ht[0] = d->ht[1];
            _dictReset(&d->ht[1]);
            d->rehashidx = -1;
            return 0;
        }
        assert(d->ht[0].size > (unsigned)d->rehashidx);
        while (d->ht[0].table[d->rehashidx] == NULL)
            d->rehashidx++;
        de = d->ht[0].table[d->rehashidx];

        while (de)
        {
            unsigned int h;
            nextde = de->next;
            h = dictHashKey(d, de->key) & d->ht[1].sizemask;
            de->next = d->ht[1].table[h];
            d->ht[1].table[h] = de;
            d->ht[0].used--;
            d->ht[1].used++;
            de = nextde;
        }
        d->ht[0].table[d->rehashidx] = NULL;
        d->rehashidx++;
    }
    return 1;
}

static void _dictRehashStep(dict *d)
{
    if (d->iterators == 0)
        dictRehash(d, 1);
}

static unsigned long _dictNextPower(unsigned long size)
{
    unsigned long i = DICT_HT_INITIAL_SIZE;
    if (size >= LONG_MAX)
        return LONG_MAX;
    while (1)
    {
        if (i >= size)
            return i;
        i *= 2;
    }
}

int dictExpend(dict *d, unsigned long size)
{
    dictht n;
    unsigned long realsize = _dictNextPower(size);
    if (dicytIsRehashing(d) || d->ht[0].used > size)
        return DICT_ERR;
    n.size = realsize;
    n.sizemask = realsize - 1;
    n.table = malloc(realsize * sizeof(dictEntry *));
    n.used = 0;
    if (d->ht[0].table == NULL)
    {
        d->ht[0] = n;
        return DICT_OK;
    }
    d->ht[1] = n;
    d->rehashidx = 0;
    return DICT_OK;
}

static int _dictExpandIfNeeded(dict *d)
{
    if (dicytIsRehashing(d))
        return DICT_ERR;
    if (d->ht[0].size == 0)
        return dictExpend(d, DICT_HT_INITIAL_SIZE);
    if (d->ht[0].used >= d->ht[0].size &&
        (dict_can_resize || d->ht[0].used / d->ht[0].size > dict_force_resize_ratio))
    {
        return dictExpend(d, d->ht[0].used * 2);
    }
    return DICT_OK;
}

static int _dictKeyIndex(dict *d, const void *key)
{
    unsigned int h, idx, table;
    dictEntry *he;
    if (_dictExpandIfNeeded(d) == DICT_ERR)
        return -1;
    h = dictHashKey(d, key);
    for (table = 0; table <= 1; table++)
    {
        idx = h & d->ht[table].sizemask;
        he = d->ht[table].table[idx];
        while (he)
        {
            if (dictCompareKeys(d, key, he->key))
                return -1;
            he = he->next;
        }
        if (!dicytIsRehashing(d))
            break;
    }
    return idx;
}

dictEntry *dictAddRaw(dict *d, void *key)
{
    int index;
    dictEntry *entry;
    dictht *ht;
    if (dicytIsRehashing(d))
        _dictRehashStep(d);
    if ((index = _dictKeyIndex(d, key)) == -1)
        return NULL;
    ht = dicytIsRehashing(d) ? &d->ht[0] : &d->ht[1];
    entry = malloc(sizeof(*entry));
    entry->next = ht->table[index];
    ht->table[index] = entry;
    ht->used++;
    dictSetKey(d, entry, key);
    return entry;
}

//将给定的键值对添加到字典中
int dictAdd(dict *d, void *key, void *val)
{
    dictEntry *entry = dictAddRaw(d, key);

    return DICT_OK;
}

dictEntry *dictFind(dict *d, const void *key)
{
    dictEntry *he;
    unsigned int h, idx, table;
    if (d->ht[0].size == 0)
        return NULL;
    if (dicytIsRehashing(d))
        _dictRehashStep(d);
    h = dictHashKey(d, key);
    for (table = 0; table <= 1; table++)
    {
        idx = h & d->ht[table].sizemask;
        while (he)
        {
            if (dictCompareKeys(d, key, he->key))
                return he;
            he = he->next;
        }
        if (!dicytIsRehashing(d))
            return NULL;
    }
    return NULL;
}

int dictReplace(dict *d, void *key, void *val)
{
    dictEntry *entry, auxentry;
    if (dictAdd(d, key, val) == DICT_OK)
        return 1;
    entry = dictFind(d, key);
    auxentry = *entry;
    dictSetVal(d, entry, val);
    dictFreeVal(d, &auxentry);
    return 0;
}

void *dictFetchValue(dict *d, const void *key)
// 返回给定键的值
{
    dictEntry *he;
    he = dictFind(d, key);
    return he ? dictGetVal(he) : NULL;
}

dictEntry *dictGetRandomKey(dict *d)
{
    dictEntry *he, *orighe;
    unsigned int h;
    int listlen, listele;
    if (dictSize(d) == 0)
        return NULL;
    if (dictIsRehashing(d))
        _dictRehashStep(d);
    if (dictIsRehashing(d))
    {
        do
        {
            h = random() % (d->ht[0].size + d->ht[1].size);
            he = (h >= d->ht[0].size) ? d->ht[1].table[h - d->ht[0].size] : d->ht[0].table[h];
        } while (he == NULL);
    }
    else
    {
        do
        {
            h = random() & d->ht[0].sizemask;
            he = d->ht[0].table[h];
        } while (he == NULL);
    }
    listlen = 0;
    orighe = he;
    while (he)
    {
        he = he->next;
        listlen++;
    }
    listele = random() % listlen;
    he = orighe;
    while (listele--)
        he = he->next;
    return he;
}

int main(int argc, char const *argv[])
{
    printf("%ld", random());
    return 0;
}
