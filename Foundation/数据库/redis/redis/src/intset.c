#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "intset.h"
#include "zmalloc.h"
#include "endianconv.h"
#include "redisassert.h"

/* Note that these encodings are ordered, so:
 * INTSET_ENC_INT16 < INTSET_ENC_INT32 < INTSET_ENC_INT64. */
#define INTSET_ENC_INT16 (sizeof(int16_t))
#define INTSET_ENC_INT32 (sizeof(int32_t))
#define INTSET_ENC_INT64 (sizeof(int64_t))

/* 获取插入元素编码 */
static uint8_t _intsetValueEncoding(int64_t v) {
    if (v < INT32_MIN || v > INT32_MAX)
        return INTSET_ENC_INT64;
    else if (v < INT16_MIN || v > INT16_MAX)
        return INTSET_ENC_INT32;
    else
        return INTSET_ENC_INT16;
}

/* Return the value at pos, given an encoding. */
static int64_t _intsetGetEncoded(intset *is, int pos, uint8_t enc) {
    int64_t v64;
    int32_t v32;
    int16_t v16;

    if (enc == INTSET_ENC_INT64) {
        memcpy(&v64, ((int64_t *) is->contents) + pos, sizeof(v64));
        memrev64ifbe(&v64);
        return v64;
    } else if (enc == INTSET_ENC_INT32) {
        memcpy(&v32, ((int32_t *) is->contents) + pos, sizeof(v32));
        memrev32ifbe(&v32);
        return v32;
    } else {
        memcpy(&v16, ((int16_t *) is->contents) + pos, sizeof(v16));
        memrev16ifbe(&v16);
        return v16;
    }
}

/* Return the value at pos, using the configured encoding. */
static int64_t _intsetGet(intset *is, int pos) {
    return _intsetGetEncoded(is, pos, intrev32ifbe(is->encoding));
}

/* Set the value at pos, using the configured encoding. */
static void _intsetSet(intset *is, int pos, int64_t value) {
    uint32_t encoding = intrev32ifbe(is->encoding);

    if (encoding == INTSET_ENC_INT64) {
        //根据偏移量 pos，通过在转换后的 int64_t 类型指针前加上 [pos]，来获取偏移后的指针位置。最后将 value 赋值给该位置
        ((int64_t *) is->contents)[pos] = value;
        memrev64ifbe(((int64_t *) is->contents) + pos);
    } else if (encoding == INTSET_ENC_INT32) {
        ((int32_t *) is->contents)[pos] = value;
        memrev32ifbe(((int32_t *) is->contents) + pos);
    } else {
        ((int16_t *) is->contents)[pos] = value;
        memrev16ifbe(((int16_t *) is->contents) + pos);
    }
}

/* Create an empty intset. */
intset *intsetNew(void) {
    intset *is = zmalloc(sizeof(intset));
    is->encoding = intrev32ifbe(INTSET_ENC_INT16);
    is->length = 0;
    return is;
}

/* 重新分配空间 */
static intset *intsetResize(intset *is, uint32_t len) {
    uint64_t size = (uint64_t) len * intrev32ifbe(is->encoding);
    assert(size <= SIZE_MAX - sizeof(intset));
    is = zrealloc(is, sizeof(intset) + size);
    return is;
}

/* 二分法查找元素 */
static uint8_t intsetSearch(intset *is, int64_t value, uint32_t *pos) {
    int min = 0, max = intrev32ifbe(is->length) - 1, mid = -1;
    int64_t cur = -1;

    /* intset为空,返回0 */
    if (intrev32ifbe(is->length) == 0) {
        if (pos) *pos = 0;
        return 0;
    } else {
        /* intset不为空,但是元素数值大于最大值或最小值时,返回0 */
        if (value > _intsetGet(is, max)) {
            //pos插入位置为is->length
            if (pos) *pos = intrev32ifbe(is->length);
            return 0;
        } else if (value < _intsetGet(is, 0)) {
            if (pos) *pos = 0;
            return 0;
        }
    }

    while (max >= min) {
        mid = ((unsigned int) min + (unsigned int) max) >> 1;
        cur = _intsetGet(is, mid);
        if (value > cur) {
            min = mid + 1;
        } else if (value < cur) {
            max = mid - 1;
        } else {
            break;
        }
    }

    if (value == cur) {
        if (pos) *pos = mid;
        return 1;
    } else {
        if (pos) *pos = min;
        return 0;
    }
}

/* 将 intset 升级为更大的编码并插入给定的整数。 */
static intset *intsetUpgradeAndAdd(intset *is, int64_t value) {
    uint8_t cur_enc = intrev32ifbe(is->encoding);
    uint8_t new_enc = _intsetValueEncoding(value);
    int length = intrev32ifbe(is->length);
    int prepend = value < 0 ? 1 : 0; //为1代表插入头部

    /* 设置intset新编码,并分配空间 */
    is->encoding = intrev32ifbe(new_enc);
    is = intsetResize(is, intrev32ifbe(is->length) + 1);

    /* 将intset元素移动到新的位置,因为新元素的编码级别比原有元素都要高,所以要么是最大的,要么是最小的.
     * 如果插入头部,就要length + prepend预留一个位置
     * */
    while (length--)
        _intsetSet(is, length + prepend, _intsetGetEncoded(is, length, cur_enc));

    if (prepend)
        //插入头部
        _intsetSet(is, 0, value);
    else
        _intsetSet(is, intrev32ifbe(is->length), value);
    //length+=1
    is->length = intrev32ifbe(intrev32ifbe(is->length) + 1);
    return is;
}

static void intsetMoveTail(intset *is, uint32_t from, uint32_t to) {
    void *src, *dst;
    uint32_t bytes = intrev32ifbe(is->length) - from; //后驱节点的长度
    uint32_t encoding = intrev32ifbe(is->encoding); //获取编码长度

    if (encoding == INTSET_ENC_INT64) {
        src = (int64_t *) is->contents + from;
        dst = (int64_t *) is->contents + to;
        bytes *= sizeof(int64_t);
    } else if (encoding == INTSET_ENC_INT32) {
        src = (int32_t *) is->contents + from;
        dst = (int32_t *) is->contents + to;
        bytes *= sizeof(int32_t);
    } else {
        src = (int16_t *) is->contents + from;
        dst = (int16_t *) is->contents + to;
        bytes *= sizeof(int16_t);
    }
    memmove(dst, src, bytes);//内存移动
}

/* 插入元素到intset中 */
intset *intsetAdd(intset *is, int64_t value, uint8_t *success) {
    uint8_t val_enc = _intsetValueEncoding(value);
    uint32_t pos;
    if (success) *success = 1;

    /* 如果插入元素的编码级别高于当前的编码,则需要升级intset编码 */
    if (val_enc > intrev32ifbe(is->encoding)) {
        /* This always succeeds, so we don't need to curry *success. */
        return intsetUpgradeAndAdd(is, value);
    } else {
        /* intsetSearch使用二分法查找元素,如果元素已存在,插入失败. */
        if (intsetSearch(is, value, &pos)) {
            if (success) *success = 0;
            return is;
        }
        //为intset重新分配内存空间,主要是分配插入元素所需空间
        is = intsetResize(is, intrev32ifbe(is->length) + 1);
        //如果存在后驱节点,则将插入位置后面所有节点后移
        if (pos < intrev32ifbe(is->length)) intsetMoveTail(is, pos, pos + 1);
    }

    _intsetSet(is, pos, value);
    //length+=1
    is->length = intrev32ifbe(intrev32ifbe(is->length) + 1);
    return is;
}

/* Delete integer from intset */
intset *intsetRemove(intset *is, int64_t value, int *success) {
    uint8_t val_enc = _intsetValueEncoding(value); //获取编码
    uint32_t pos;
    if (success) *success = 0;
    //如果value在intset中
    if (val_enc <= intrev32ifbe(is->encoding) && intsetSearch(is, value, &pos)) {
        uint32_t len = intrev32ifbe(is->length);

        /* We know we can delete */
        if (success) *success = 1;

        /* 如果有后驱节点,内存数据往前移动 */
        if (pos < (len - 1)) intsetMoveTail(is, pos + 1, pos);
        is = intsetResize(is, len - 1);
        is->length = intrev32ifbe(len - 1);
    }
    return is;
}

/* 判断一个值是否属于这个集合 */
uint8_t intsetFind(intset *is, int64_t value) {
    uint8_t valenc = _intsetValueEncoding(value);
    return valenc <= intrev32ifbe(is->encoding) && intsetSearch(is, value, NULL);
}

/* 获取一个随机值 */
int64_t intsetRandom(intset *is) {
    return _intsetGet(is, rand() % intrev32ifbe(is->length));
}

/*获取给定位置的值。 当该位置超出范围时，该函数返回 0，当该位置在范围内时，该函数返回 1。 */
uint8_t intsetGet(intset *is, uint32_t pos, int64_t *value) {
    if (pos < intrev32ifbe(is->length)) {
        *value = _intsetGet(is, pos);
        return 1;
    }
    return 0;
}

/* 返回intset长度 */
uint32_t intsetLen(const intset *is) {
    return intrev32ifbe(is->length);
}

/* Return intset blob size in bytes. */
size_t intsetBlobLen(intset *is) {
    return sizeof(intset) + intrev32ifbe(is->length) * intrev32ifbe(is->encoding);
}

#ifdef REDIS_TEST
#include <sys/time.h>
#include <time.h>

#if 0
static void intsetRepr(intset *is) {
    for (uint32_t i = 0; i < intrev32ifbe(is->length); i++) {
        printf("%lld\n", (uint64_t)_intsetGet(is,i));
    }
    printf("\n");
}

static void error(char *err) {
    printf("%s\n", err);
    exit(1);
}
#endif

static void ok(void) {
    printf("OK\n");
}

static long long usec(void) {
    struct timeval tv;
    gettimeofday(&tv,NULL);
    return (((long long)tv.tv_sec)*1000000)+tv.tv_usec;
}

#define assert(_e) ((_e)?(void)0:(_assert(#_e,__FILE__,__LINE__),exit(1)))
static void _assert(char *estr, char *file, int line) {
    printf("\n\n=== ASSERTION FAILED ===\n");
    printf("==> %s:%d '%s' is not true\n",file,line,estr);
}

static intset *createSet(int bits, int size) {
    uint64_t mask = (1<<bits)-1;
    uint64_t value;
    intset *is = intsetNew();

    for (int i = 0; i < size; i++) {
        if (bits > 32) {
            value = (rand()*rand()) & mask;
        } else {
            value = rand() & mask;
        }
        is = intsetAdd(is,value,NULL);
    }
    return is;
}

static void checkConsistency(intset *is) {
    for (uint32_t i = 0; i < (intrev32ifbe(is->length)-1); i++) {
        uint32_t encoding = intrev32ifbe(is->encoding);

        if (encoding == INTSET_ENC_INT16) {
            int16_t *i16 = (int16_t*)is->contents;
            assert(i16[i] < i16[i+1]);
        } else if (encoding == INTSET_ENC_INT32) {
            int32_t *i32 = (int32_t*)is->contents;
            assert(i32[i] < i32[i+1]);
        } else {
            int64_t *i64 = (int64_t*)is->contents;
            assert(i64[i] < i64[i+1]);
        }
    }
}

#define UNUSED(x) (void)(x)
int intsetTest(int argc, char **argv) {
    uint8_t success;
    int i;
    intset *is;
    srand(time(NULL));

    UNUSED(argc);
    UNUSED(argv);

    printf("Value encodings: "); {
        assert(_intsetValueEncoding(-32768) == INTSET_ENC_INT16);
        assert(_intsetValueEncoding(+32767) == INTSET_ENC_INT16);
        assert(_intsetValueEncoding(-32769) == INTSET_ENC_INT32);
        assert(_intsetValueEncoding(+32768) == INTSET_ENC_INT32);
        assert(_intsetValueEncoding(-2147483648) == INTSET_ENC_INT32);
        assert(_intsetValueEncoding(+2147483647) == INTSET_ENC_INT32);
        assert(_intsetValueEncoding(-2147483649) == INTSET_ENC_INT64);
        assert(_intsetValueEncoding(+2147483648) == INTSET_ENC_INT64);
        assert(_intsetValueEncoding(-9223372036854775808ull) ==
                    INTSET_ENC_INT64);
        assert(_intsetValueEncoding(+9223372036854775807ull) ==
                    INTSET_ENC_INT64);
        ok();
    }

    printf("Basic adding: "); {
        is = intsetNew();
        is = intsetAdd(is,5,&success); assert(success);
        is = intsetAdd(is,6,&success); assert(success);
        is = intsetAdd(is,4,&success); assert(success);
        is = intsetAdd(is,4,&success); assert(!success);
        ok();
    }

    printf("Large number of random adds: "); {
        uint32_t inserts = 0;
        is = intsetNew();
        for (i = 0; i < 1024; i++) {
            is = intsetAdd(is,rand()%0x800,&success);
            if (success) inserts++;
        }
        assert(intrev32ifbe(is->length) == inserts);
        checkConsistency(is);
        ok();
    }

    printf("Upgrade from int16 to int32: "); {
        is = intsetNew();
        is = intsetAdd(is,32,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT16);
        is = intsetAdd(is,65535,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT32);
        assert(intsetFind(is,32));
        assert(intsetFind(is,65535));
        checkConsistency(is);

        is = intsetNew();
        is = intsetAdd(is,32,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT16);
        is = intsetAdd(is,-65535,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT32);
        assert(intsetFind(is,32));
        assert(intsetFind(is,-65535));
        checkConsistency(is);
        ok();
    }

    printf("Upgrade from int16 to int64: "); {
        is = intsetNew();
        is = intsetAdd(is,32,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT16);
        is = intsetAdd(is,4294967295,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT64);
        assert(intsetFind(is,32));
        assert(intsetFind(is,4294967295));
        checkConsistency(is);

        is = intsetNew();
        is = intsetAdd(is,32,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT16);
        is = intsetAdd(is,-4294967295,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT64);
        assert(intsetFind(is,32));
        assert(intsetFind(is,-4294967295));
        checkConsistency(is);
        ok();
    }

    printf("Upgrade from int32 to int64: "); {
        is = intsetNew();
        is = intsetAdd(is,65535,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT32);
        is = intsetAdd(is,4294967295,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT64);
        assert(intsetFind(is,65535));
        assert(intsetFind(is,4294967295));
        checkConsistency(is);

        is = intsetNew();
        is = intsetAdd(is,65535,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT32);
        is = intsetAdd(is,-4294967295,NULL);
        assert(intrev32ifbe(is->encoding) == INTSET_ENC_INT64);
        assert(intsetFind(is,65535));
        assert(intsetFind(is,-4294967295));
        checkConsistency(is);
        ok();
    }

    printf("Stress lookups: "); {
        long num = 100000, size = 10000;
        int i, bits = 20;
        long long start;
        is = createSet(bits,size);
        checkConsistency(is);

        start = usec();
        for (i = 0; i < num; i++) intsetSearch(is,rand() % ((1<<bits)-1),NULL);
        printf("%ld lookups, %ld element set, %lldusec\n",
               num,size,usec()-start);
    }

    printf("Stress add+delete: "); {
        int i, v1, v2;
        is = intsetNew();
        for (i = 0; i < 0xffff; i++) {
            v1 = rand() % 0xfff;
            is = intsetAdd(is,v1,NULL);
            assert(intsetFind(is,v1));

            v2 = rand() % 0xfff;
            is = intsetRemove(is,v2,NULL);
            assert(!intsetFind(is,v2));
        }
        checkConsistency(is);
        ok();
    }

    return 0;
}
#endif
