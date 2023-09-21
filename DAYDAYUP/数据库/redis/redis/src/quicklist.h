/* quicklist.h - A generic doubly linked quicklist implementation
 */

#ifndef __QUICKLIST_H__
#define __QUICKLIST_H__

typedef struct quicklistNode {
    struct quicklistNode *prev; //前一个quicklistNode
    struct quicklistNode *next; //后一个quicklistNode
    unsigned char *zl; //quicklistNode指向的ziplist
    unsigned int sz;             /* ziplist的字节大小 */
    unsigned int count: 16;     /* ziplist中的元素个数 */
    unsigned int encoding: 2;   /*编码格式,原生字节数组或压缩存储 RAW==1 or LZF==2 */
    unsigned int container: 2;  /*存储方式 NONE==1 or ZIPLIST==2 */
    unsigned int recompress: 1; /* 数据是否被压缩 */
    unsigned int attempted_compress: 1; /* 数据能否被压缩 */
    unsigned int extra: 10; /* 预留的bit位 */
} quicklistNode;

/* quicklistLZF is a 4+N byte struct holding 'sz' followed by 'compressed'.
 * 'sz' is byte length of 'compressed' field.
 * 'compressed' is LZF data with total (compressed) length 'sz'
 * NOTE: uncompressed length is stored in quicklistNode->sz.
 * When quicklistNode->zl is compressed, node->zl points to a quicklistLZF */
typedef struct quicklistLZF {
    unsigned int sz; /* 压缩后的ziplist 大小 */
    char compressed[]; //存放压缩后的ziplist字节数组
} quicklistLZF;


typedef struct quicklist {
    quicklistNode *head;          //quicklist链表头
    quicklistNode *tail;          //quicklist链表尾
    unsigned long count;        /* 所有ziplist中的总元素个数 */
    unsigned long len;          /* 节点数量 */
    int fill: 16;              /* fill：用于判断节点的ziplist是否已满*/
    unsigned int compress: 16; /* 存放节点压缩配置;0=off */
} quicklist;

typedef struct quicklistIter {
    const quicklist *quicklist;
    quicklistNode *current;
    unsigned char *zi;
    long offset; /* offset in current ziplist */
    int direction;
} quicklistIter;

typedef struct quicklistEntry {
    const quicklist *quicklist;
    quicklistNode *node;
    unsigned char *zi;
    unsigned char *value;
    long long longval;
    unsigned int sz;
    int offset;
} quicklistEntry;

#define QUICKLIST_HEAD 0
#define QUICKLIST_TAIL -1

/* quicklist node encodings */
#define QUICKLIST_NODE_ENCODING_RAW 1
#define QUICKLIST_NODE_ENCODING_LZF 2

/* quicklist compression disable */
#define QUICKLIST_NOCOMPRESS 0

/* quicklist container formats */
#define QUICKLIST_NODE_CONTAINER_NONE 1
#define QUICKLIST_NODE_CONTAINER_ZIPLIST 2

#define quicklistNodeIsCompressed(node)                                        \
    ((node)->encoding == QUICKLIST_NODE_ENCODING_LZF)

/* Prototypes */
quicklist *quicklistCreate(void);

quicklist *quicklistNew(int fill, int compress);

void quicklistSetCompressDepth(quicklist *quicklist, int depth);

void quicklistSetFill(quicklist *quicklist, int fill);

void quicklistSetOptions(quicklist *quicklist, int fill, int depth);

void quicklistRelease(quicklist *quicklist);

int quicklistPushHead(quicklist *quicklist, void *value, const size_t sz);

int quicklistPushTail(quicklist *quicklist, void *value, const size_t sz);

void quicklistPush(quicklist *quicklist, void *value, const size_t sz,
                   int where);

void quicklistAppendZiplist(quicklist *quicklist, unsigned char *zl);

quicklist *quicklistAppendValuesFromZiplist(quicklist *quicklist,
                                            unsigned char *zl);

quicklist *quicklistCreateFromZiplist(int fill, int compress,
                                      unsigned char *zl);

void quicklistInsertAfter(quicklist *quicklist, quicklistEntry *node,
                          void *value, const size_t sz);

void quicklistInsertBefore(quicklist *quicklist, quicklistEntry *node,
                           void *value, const size_t sz);

void quicklistDelEntry(quicklistIter *iter, quicklistEntry *entry);

int quicklistReplaceAtIndex(quicklist *quicklist, long index, void *data,
                            int sz);

int quicklistDelRange(quicklist *quicklist, const long start, const long stop);

quicklistIter *quicklistGetIterator(const quicklist *quicklist, int direction);

quicklistIter *quicklistGetIteratorAtIdx(const quicklist *quicklist,
                                         int direction, const long long idx);

int quicklistNext(quicklistIter *iter, quicklistEntry *node);

void quicklistReleaseIterator(quicklistIter *iter);

quicklist *quicklistDup(quicklist *orig);

int quicklistIndex(const quicklist *quicklist, const long long index,
                   quicklistEntry *entry);

void quicklistRewind(quicklist *quicklist, quicklistIter *li);

void quicklistRewindTail(quicklist *quicklist, quicklistIter *li);

void quicklistRotate(quicklist *quicklist);

int quicklistPopCustom(quicklist *quicklist, int where, unsigned char **data,
                       unsigned int *sz, long long *sval,
                       void *(*saver)(unsigned char *data, unsigned int sz));

int quicklistPop(quicklist *quicklist, int where, unsigned char **data,
                 unsigned int *sz, long long *slong);

unsigned long quicklistCount(const quicklist *ql);

int quicklistCompare(unsigned char *p1, unsigned char *p2, int p2_len);

size_t quicklistGetLzf(const quicklistNode *node, void **data);

#ifdef REDIS_TEST
int quicklistTest(int argc, char *argv[]);
#endif

/* Directions for iterators */
#define AL_START_HEAD 0
#define AL_START_TAIL 1

#endif /* __QUICKLIST_H__ */
