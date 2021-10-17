#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define REDIS_LRU_BITS 24
#define ZSKIPLIST_MAXLEVEL 32

typedef struct redisObject
{
    unsigned type : 4;
    unsigned encoding : 4;
    unsigned lru : REDIS_LRU_BITS;
    int refcount;
    void *prt;
} robj;

typedef struct zskiplistNode
{
    robj *obj;
    double score;
    struct zskiplistNode *backward;
    struct zskiplistLevel
    {
        struct zskiplistNode *forward;
        unsigned int span;
    } level[];
} zskiplistNode;

typedef struct zskiplist
{
    struct zskiplistNode *header, *tail;
    unsigned long length;
    int level;
} zskiplist;

zskiplistNode *zslCreateNode(int level, double score, robj *obj)
{
    zskiplistNode *zn = malloc(sizeof(*zn) + level * sizeof(struct zskiplistLevel));
    zn->score = score;
    zn->obj = obj;
    return zn;
}

zskiplist *zslCreate(void)
//创建一个新的跳表
{
    int j;
    zskiplist *zsl;
    zsl = malloc(sizeof(*zsl));
    zsl->length = 0;
    zsl->level = 1;
    zsl->header = zslCreateNode(ZSKIPLIST_MAXLEVEL, 0, NULL);
    for (j = 0; j < ZSKIPLIST_MAXLEVEL; j++)
    {
        zsl->header->level[j].forward = NULL;
        zsl->header->level[j].span = 0;
    }
    zsl->header->backward = NULL;
    zsl->tail = NULL;
    return zsl;
}

int main(int argc, char const *argv[])
{
    /* code */
    return 0;
}
