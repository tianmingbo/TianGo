#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <limits.h>
#define DICT_OK 0
#define DICT_ERR 1

#define dicytIsRehashing(ht) ((ht)->rehashidx != -1)
#define dictHashKey(d, key) (d)->type->hashFunction(key)
#define DICT_HT_INITIAL_SIZE 4
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
    
}

dictEntry *dictAddRaw(dict *d, void *key)
{
    int index;
    dictEntry *entry;
    dictht *ht;
    if (dicytIsRehashing(d))
        _dictRehashStep(d);
}

int dictAdd(dict *d, void *key, void *val)
{
    dictEntry *entry = dictAddRaw(d, key);

    return DICT_OK;
}