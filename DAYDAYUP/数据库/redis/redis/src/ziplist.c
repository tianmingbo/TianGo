/* ziplist是一个特殊编码的双链表，其设计目的是
  * 内存效率非常高。 它存储字符串和整数值，
  * 其中整数被编码为实际整数而不是一系列
  * 人物。 它允许在列表的两侧进行推送和弹出操作
  * 在 O(1) 时间内。 然而，由于每次操作都需要重新分配
  * ziplist使用的内存，实际复杂度与
  * ziplist 使用的内存量。
  *
  * ------------------------------------------------- ----------------------------
  *
  * Ziplist 整体布局
  *======================
  *
  * ziplist的总体布局如下：
  *
  * <zlbytes> <zltail> <zllen> <entry> <entry> ... <entry> <zlend>
  *
  * 注意：如果没有另外指定，所有字段都以小端存储。
  *
  * <uint32_t zlbytes> 是一个无符号整数，用于保存字节数
  * ziplist占用，包括zlbytes字段本身的四个字节。
  * 需要存储该值才能调整整个结构的大小
  * 无需先遍历它。
  *
  * <uint32_t zltail> 是列表中最后一个entry的偏移量。 这允许
  * 在列表的远端进行弹出操作，无需完整操作
  * 遍历。
  *
  * <uint16_t zllen> 是entry数。 当有超过
  * 2^16-2个entry，这个值设置为2^16-1，我们需要遍历
  * 整个列表以了解它包含多少项目。
  *
  * <uint8_t zlend> 是一个特殊entry，表示 ziplist 的末尾。
  * 被编码为等于 255 的单个字节。没有其他正常entry启动
  * 将字节值设置为 255。
  *
  * 压缩列表entry
  * ===============
  *
  * ziplist 中的每个entry都以包含两部分的元数据为前缀
  * 信息。 首先，前一个entry的长度被存储为
  * 能够从后向前遍历列表。 二、entry编码为
  * 假如。 它表示entry类型，整数或字符串，在这种情况下
  * 字符串的它也代表字符串有效负载的长度。
  * 所以一个完整的entry是这样存储的：
  *
  * <prevlen> <编码> <entry数据>
  *
  * 有时编码代表entry本身，例如小整数
  * 我们稍后会看到。 在这种情况下， <entry-data> 部分丢失，我们
  * 可能只是：
  *
  * <prevlen> <编码>
  *
  * 前一个entry的长度 <prevlen> 按以下方式编码：
  * 如果这个长度小于254字节，则只会消耗单个
  * 将长度表示为无符号 8 位整数的字节。 当长度
  * 大于或等于254，将消耗5个字节。 第一个字节是
  * 设置为 254 (FE) 表示后面有更大的值。 剩余 4 个
  * bytes 将前一个entry的长度作为值。
  *
  * 因此，实际上一个entry是按以下方式编码的：
  *
  * <prevlen 从 0 到 253> <编码> <entry>
  *
  * 或者如果前一个entry长度大于 253 字节
  * 使用以下编码：
  *
  * 0xFE <4 字节无符号小端 prevlen> <编码> <entry>
  *
  * entry的编码字段取决于entry的内容
  * 入口。 当entry是字符串时，先编码前2位
  * byte 将保存用于存储字符串长度的编码类型，
  * 后跟字符串的实际长度。 当entry是整数时
  * 前2位均设置为1。后面2位用于指定
  * 该标头之后将存储什么样的整数。 概述
  * 不同类型和编码如下。 第一个字节总是足够的
  * 确定entry的类型。
 *
 * |00pppppp| - 1 字节
  * 长度小于或等于63字节（6位）的字符串值。
  * “pppppp”表示无符号6位长度。
  * |01pppppp|QQQQQQQQ| - 2字节
  * 长度小于或等于16383字节（14位）的字符串值。
  * 重要提示：14 位数字以大端存储。
  * |10000000|qqqqqqqq|rrrrrrrr|ssssssss|tttttttt| - 5字节
  * 长度大于或等于16384字节的字符串值。
  * 仅第一个字节后面的4个字节代表长度
  * 最多 32^2-1。 第一个字节的低 6 位未被使用，
  * 设置为零。
  * 重要提示：32 位数字以大端存储。
  * |11000000| - 3字节
  * 整数编码为 int16_t（2 个字节）。
  * |11010000| - 5字节
  * 整数编码为 int32_t（4 个字节）。
  * |11100000| - 9 字节
  * 整数编码为 int64_t（8 字节）。
  * |11110000| - 4字节
  * 整数编码为 24 位有符号（3 个字节）。
  * |11111110| - 2字节
  * 整数编码为 8 位有符号（1 字节）。
  * |1111xxxx| - （xxxx 在 0000 到 1101 之间）立即数 4 位整数。
  * 从0到12的无符号整数。编码值实际上是从
  * 1到13因为0000和1111不能使用，所以应该是1
  * 从编码的 4 位值中减去以获得正确的值。
  * |11111111| - ziplist 特殊entry结束。
  *
  * 与 ziplist 标头一样，所有整数都以小数表示
  * endian 字节顺序，即使此代码是在大 endian 系统中编译的。
  *
  * 实际 ziplist 的示例
  * ===========================
  *
  * 下面是一个ziplist，其中包含代表的两个元素
  * 字符串“2”和“5”。 它由15个字节组成，我们直观地
  * 分成几个部分：
  *
  * [0f 00 00 00] [0c 00 00 00] [02 00] [00 f3] [02 f6] [ff]
  * | | | | | |
  * zlbytes zltailentry“2”“5”结束
  *
  * 前4个字节代表数字15，即字节数
  * 整个ziplist由. 第二个4字节是偏移量
  * 找到最后一个 ziplist entry，即 12，实际上是
  * 最后一个entry，即“5”，位于 ziplist 内的偏移量 12 处。
  * 接下来的16位整数表示内部元素的数量
  * ziplist，它的值为2，因为里面只有两个元素。
  * 最后“00 f3”是代表数字2的第一个entry。它是
  * 由前一个entry长度组成，该长度为零，因为这是
  * 我们的第一个entry，以及对应于编码的字节 F3
  * |1111xxxx| xxxx在0001和1101之间。我们需要删除“F”
  * 高位1111，并从“3”中减去1，所以entry值
  * 是“2”。 下一个entry的 prevlen 为 02，因为第一个entry是
  * 由两个字节组成。 entry本身 F6 被精确编码
  * 与第一个entry类似，并且 6-1 = 5，因此该entry的值为 5。
  * 最后，特殊entry FF 表示 ziplist 的结束。
  *
  * 将另一个元素添加到上面的字符串中，其值为“Hello World”
  * 允许我们展示 ziplist 如何对小字符串进行编码。 我们只会展示
  * entry本身的十六进制转储。 想象一下字节如下
  * 在上面的 ziplist 中存储“5”的entry：
  *
  * [02] [0b] [48 65 6c 6c 6f 20 57 6f 72 6c 64]
  *
  * 第一个字节 02 是前一个entry的长度。 下一个
  * byte 表示模式 |00pppppp| 中的编码 这意味着
  * 该entry是一个长度为 <pppppp> 的字符串，因此 0B 表示
  * 后面是一个 11 字节的字符串。 从第三个字节 (48) 到最后一个字节 (64)
  * 只有“Hello World”的 ASCII 字符。
  *
  */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <limits.h>
#include "zmalloc.h"
#include "util.h"
#include "ziplist.h"
#include "endianconv.h"
#include "redisassert.h"

#define ZIP_END 255         /* Special "end of ziplist" entry.  结束字符*/
#define ZIP_BIG_PREVLEN 254 /* Max number of bytes of the previous entry, for
                               the "prevlen" field prefixing each entry, to be
                               represented with just a single byte. Otherwise
                               it is represented as FF AA BB CC DD, where
                               AA BB CC DD are a 4 bytes unsigned integer
                               representing the previous entry len. */

/* Different encoding/length possibilities */
#define ZIP_STR_MASK 0xc0
#define ZIP_INT_MASK 0x30
#define ZIP_STR_06B (0 << 6) //长度字段占用 1 字节，且长度值小于等于 63（0x3f）。
#define ZIP_STR_14B (1 << 6) //长度字段占用 2 字节，长度值小于等于 16383（0x3fff）
#define ZIP_STR_32B (2 << 6) //长度字段占用 5 字节，长度值由后续的 4 字节依次拼接而成
#define ZIP_INT_16B (0xc0 | 0<<4) //11000000
#define ZIP_INT_32B (0xc0 | 1<<4) //11000000 | 00010000  11010000表示int32_t类型
#define ZIP_INT_64B (0xc0 | 2<<4) //11100000
#define ZIP_INT_24B (0xc0 | 3<<4) //11110000
#define ZIP_INT_8B 0xfe           //8位有符号整数

/* 4 bit integer immediate encoding |1111xxxx| with xxxx between
 * 0001 and 1101. */
#define ZIP_INT_IMM_MASK 0x0f   /* Mask to extract the 4 bits value. To add
                                   one is needed to reconstruct the value. */
#define ZIP_INT_IMM_MIN 0xf1    /* 11110001 */
#define ZIP_INT_IMM_MAX 0xfd    /* 11111101 */

#define INT24_MAX 0x7fffff
#define INT24_MIN (-INT24_MAX - 1)

/* Macro to determine if the entry is a string. String entries never start
 * with "11" as most significant bits of the first byte. */
#define ZIP_IS_STR(enc) (((enc) & ZIP_STR_MASK) < ZIP_STR_MASK)

/* Utility macros.*/

// 定位到 ziplist 的 bytes 属性，该属性记录了整个 ziplist 所占用的内存字节数
// 用于取出 bytes 属性的现有值，或者为 bytes 属性赋予新值
#define ZIPLIST_BYTES(zl)       (*((uint32_t*)(zl)))

// 定位到 ziplist 的 offset 属性，该属性记录了到达表尾节点的偏移量
// 用于取出 offset 属性的现有值，或者为 offset 属性赋予新值
#define ZIPLIST_TAIL_OFFSET(zl) (*((uint32_t*)((zl)+sizeof(uint32_t))))

// 定位到 ziplist 的 length 属性，该属性记录了 ziplist 包含的节点数量
// 用于取出 length 属性的现有值，或者为 length 属性赋予新值
#define ZIPLIST_LENGTH(zl)      (*((uint16_t*)((zl)+sizeof(uint32_t)*2)))

// 返回 ziplist 表头的大小
#define ZIPLIST_HEADER_SIZE     (sizeof(uint32_t)*2+sizeof(uint16_t))

/* Size of the "end of ziplist" entry. Just one byte. 1字节*/
#define ZIPLIST_END_SIZE        (sizeof(uint8_t))

/* 返回第一个entry指针 */
#define ZIPLIST_ENTRY_HEAD(zl)  ((zl)+ZIPLIST_HEADER_SIZE)

// 返回指向 ziplist 最后一个节点（的起始位置）的指
#define ZIPLIST_ENTRY_TAIL(zl)  ((zl)+intrev32ifbe(ZIPLIST_TAIL_OFFSET(zl)))

// 返回指向 ziplist 末端 ZIP_END （的起始位置）的指针
#define ZIPLIST_ENTRY_END(zl)   ((zl)+intrev32ifbe(ZIPLIST_BYTES(zl))-1)

/*
 * 增加 ziplist 的节点数
*/
#define ZIPLIST_INCR_LENGTH(zl, incr) { \
    if (intrev16ifbe(ZIPLIST_LENGTH(zl)) < UINT16_MAX) \
        ZIPLIST_LENGTH(zl) = intrev16ifbe(intrev16ifbe(ZIPLIST_LENGTH(zl))+incr); \
}

/* Don't let ziplists grow over 1GB in any case, don't wanna risk overflow in
 * zlbytes*/
#define ZIPLIST_MAX_SAFETY_SIZE (1<<30)

int ziplistSafeToAdd(unsigned char *zl, size_t add) {
    size_t len = zl ? ziplistBlobLen(zl) : 0;
    if (len + add > ZIPLIST_MAX_SAFETY_SIZE)
        return 0;
    return 1;
}


/* We use this function to receive information about a ziplist entry.
 * Note that this is not how the data is actually encoded, is just what we
 * get filled by a function in order to operate more easily. */
typedef struct zlentry {
    unsigned int prevrawlensize; /*用于编码前一个entry长度的字节数*/
    unsigned int prevrawlen;     /* 前一个entry的长度 */
    unsigned int lensize;        /* 用于编码当前entry类型和长度的字节数。例如，字符串类型的entry有1、2或5个字节的头部，而整数类型的entry始终使用一个字节*/
    unsigned int len;            /* 表示实际entry长度的字节数。对于字符串类型的entry，它等于字符串的长度；对于整数类型的entry，它可以是1、2、3、4、8或0（对于4位立即数） */
    unsigned int headersize;     /* 存储头部长度的字节数，即prevrawlensize + lensize。 */
    unsigned char encoding;      /*当前节点值所使用的编码类型*/
    unsigned char *p;            /*指向entry起始位置的指针，即指向前一个entry长度字段的位置。 */
} zlentry;

#define ZIPLIST_ENTRY_ZERO(zle) { \
    (zle)->prevrawlensize = (zle)->prevrawlen = 0; \
    (zle)->lensize = (zle)->len = (zle)->headersize = 0; \
    (zle)->encoding = 0; \
    (zle)->p = NULL; \
}

/* Extract the encoding from the byte pointed by 'ptr' and set it into
 * 'encoding' field of the zlentry structure. */
#define ZIP_ENTRY_ENCODING(ptr, encoding) do {  \
    (encoding) = (ptr[0]); \
    if ((encoding) < ZIP_STR_MASK) (encoding) &= ZIP_STR_MASK; \
} while(0)

/* Return bytes needed to store integer encoded by 'encoding'. */
unsigned int zipIntSize(unsigned char encoding) {
    switch (encoding) {
        case ZIP_INT_8B:
            return 1;
        case ZIP_INT_16B:
            return 2;
        case ZIP_INT_24B:
            return 3;
        case ZIP_INT_32B:
            return 4;
        case ZIP_INT_64B:
            return 8;
    }
    if (encoding >= ZIP_INT_IMM_MIN && encoding <= ZIP_INT_IMM_MAX)
        return 0; /* 4 bit immediate */
    panic("Invalid integer encoding 0x%02X", encoding);
    return 0;
}

/* Write the encoidng header of the entry in 'p'. If p is NULL it just returns
 * the amount of bytes required to encode such a length. Arguments:
 *
 * 'encoding' is the encoding we are using for the entry. It could be
 * ZIP_INT_* or ZIP_STR_* or between ZIP_INT_IMM_MIN and ZIP_INT_IMM_MAX
 * for single-byte small immediate integers.
 *
 * 'rawlen' is only used for ZIP_STR_* encodings and is the length of the
 * srting that this entry represents.
 *
 * The function returns the number of bytes used by the encoding/length
 * header stored in 'p'.
 *
 * 编码节点长度值 l ，并将它写入到 p 中，然后返回编码 l 所需的字节数量。
 * 如果 p 为 NULL ，那么仅返回编码 l 所需的字节数量，不进行写入。
 *
 * T = O(1)
 * */
unsigned int zipStoreEntryEncoding(unsigned char *p, unsigned char encoding, unsigned int rawlen) {
    unsigned char len = 1, buf[5];
    //编码字符串
    if (ZIP_IS_STR(encoding)) {
        /* Although encoding is given it may not be set for strings,
         * so we determine it here using the raw length. */
        //长度<63,编码长度1字节 00xxxxxx
        if (rawlen <= 0x3f) {
            if (!p) return len;
            buf[0] = ZIP_STR_06B | rawlen;
        } else if (rawlen <= 0x3fff) {
            //长度小于16383,编码长度2字节.01xxxxxx xxxxxxxx
            len += 1;
            if (!p) return len;
            buf[0] = ZIP_STR_14B | ((rawlen >> 8) & 0x3f);
            buf[1] = rawlen & 0xff;
        } else {
            //长度小于4294967295,占用5字节
            len += 4;
            if (!p) return len;
            buf[0] = ZIP_STR_32B;
            buf[1] = (rawlen >> 24) & 0xff;
            buf[2] = (rawlen >> 16) & 0xff;
            buf[3] = (rawlen >> 8) & 0xff;
            buf[4] = rawlen & 0xff;
        }
    } else {
        /* 整数的所有编码都是1Byte */
        if (!p) return len;
        buf[0] = encoding;
    }

    /* Store this length at p. */
    memcpy(p, buf, len);
    //编码所需长度
    return len;
}

/* 解码当前entry的编码、长度所占的字节数以及实际长度。
 * “encoding”变量将保存条目编码，
 * “lensize”变量将保存对条目长度进行编码所需的字节数，
 * “len”变量将保存条目长度。
 *
 * if ((encoding) < ZIP_STR_MASK)：判断编码方式是否为字符串类型
 * */
#define ZIP_DECODE_LENGTH(ptr, encoding, lensize, len) do {                    \
    ZIP_ENTRY_ENCODING((ptr), (encoding));                                     \
    if ((encoding) < ZIP_STR_MASK) {                                            \
        if ((encoding) == ZIP_STR_06B) {                                       \
            (lensize) = 1;                                                     \
            (len) = (ptr)[0] & 0x3f;                                           \
        } else if ((encoding) == ZIP_STR_14B) {                                \
            (lensize) = 2;                                                     \
            (len) = (((ptr)[0] & 0x3f) << 8) | (ptr)[1];                       \
        } else if ((encoding) == ZIP_STR_32B) {                                \
            (lensize) = 5;                                                     \
            (len) = ((ptr)[1] << 24) |                                         \
                    ((ptr)[2] << 16) |                                         \
                    ((ptr)[3] <<  8) |                                         \
                    ((ptr)[4]);                                                \
        } else {                                                               \
            panic("Invalid string encoding 0x%02X", (encoding));               \
        }                                                                      \
    } else {                                                                   \
        (lensize) = 1;                                                         \
        (len) = zipIntSize(encoding);                                          \
    }                                                                          \
} while(0);

/* Encode the length of the previous entry and write it to "p". This only
 * uses the larger encoding (required in __ziplistCascadeUpdate). */
int zipStorePrevEntryLengthLarge(unsigned char *p, unsigned int len) {
    if (p != NULL) {
        p[0] = ZIP_BIG_PREVLEN;
        memcpy(p + 1, &len, sizeof(len));
        memrev32ifbe(p + 1);
    }
    return 1 + sizeof(len);
}

/* 对前一个条目的长度进行编码并将其写入“p”。 如果“p”为 NULL，则返回编码此长度所需的字节数。 */
unsigned int zipStorePrevEntryLength(unsigned char *p, unsigned int len) {
    if (p == NULL) {
        return (len < ZIP_BIG_PREVLEN) ? 1 : sizeof(len) + 1;
    } else {
        if (len < ZIP_BIG_PREVLEN) {
            p[0] = len;
            return 1;
        } else {
            return zipStorePrevEntryLengthLarge(p, len);
        }
    }
}

/* 返回用于对前一个条目的长度进行编码的字节数。 通过设置 var 'prevlensize' 返回长度。 */
#define ZIP_DECODE_PREVLENSIZE(ptr, prevlensize) do {                          \
    if ((ptr)[0] < ZIP_BIG_PREVLEN) {                                          \
        (prevlensize) = 1;                                                     \
    } else {                                                                   \
        (prevlensize) = 5;                                                     \
    }                                                                          \
} while(0);

/* Decode the length of the previous element, from the perspective of the entry
 * pointed to by 'ptr'.
 *
 * 解码 ptr 指针，
 * 取出编码前置节点长度所需的字节数，
 * 并将这个字节数保存到 prevlensize 中。
 *
 * 然后根据 prevlensize ，从 ptr 中取出前置节点的长度值，
 * 并将这个长度值保存到 prevlen 变量中。
 *
 * T = O(1)
 */
#define ZIP_DECODE_PREVLEN(ptr, prevlensize, prevlen) do {                     \
    ZIP_DECODE_PREVLENSIZE(ptr, prevlensize);                                  \
    if ((prevlensize) == 1) {                                                  \
        (prevlen) = (ptr)[0];                                                  \
    } else if ((prevlensize) == 5) {                                           \
        assert(sizeof((prevlen)) == 4);                                    \
        memcpy(&(prevlen), ((char*)(ptr)) + 1, 4);                             \
        memrev32ifbe(&prevlen);                                                \
    }                                                                          \
} while(0);

/* 计算编码新的前置节点长度 len 所需的字节数，
 * 减去编码 p 原来的前置节点长度所需的字节数之差。
 * */
int zipPrevLenByteDiff(unsigned char *p, unsigned int len) {
    unsigned int prevlensize;
    ZIP_DECODE_PREVLENSIZE(p, prevlensize);
    return zipStorePrevEntryLength(NULL, len) - prevlensize;
}

/* 计算当前指针 p 指向的entry 的原始长度 */
unsigned int zipRawEntryLength(unsigned char *p) {
    unsigned int prevlensize, encoding, lensize, len;
    ZIP_DECODE_PREVLENSIZE(p, prevlensize);  // 解码前一个条目长度所占的字节数
    ZIP_DECODE_LENGTH(p + prevlensize, encoding, lensize, len);
    return prevlensize + lensize + len; //返回entry总长度
}

/* Check if string pointed to by 'entry' can be encoded as an integer.
 * Stores the integer value in 'v' and its encoding in 'encoding'.
 *  * 检查 entry 中指向的字符串能否被编码为整数。
 *
 * 如果可以的话，
 * 将编码后的整数保存在指针 v 的值中，并将编码的方式保存在指针 encoding 的值中。
 *
 * 注意，这里的 entry 和前面代表节点的 entry 不是一个意思。这里的entry是传入的字符
 *
 * T = O(N)
 * */
int zipTryEncoding(unsigned char *entry, unsigned int entrylen, long long *v, unsigned char *encoding) {
    long long value;

    if (entrylen >= 32 || entrylen == 0) return 0; //字符串太长或太短，转整型无意义
    if (string2ll((char *) entry, entrylen, &value)) {
        /* Great, the string can be encoded. Check what's the smallest
         * of our encoding types that can hold this value. */
        if (value >= 0 && value <= 12) {
            *encoding = ZIP_INT_IMM_MIN + value;
        } else if (value >= INT8_MIN && value <= INT8_MAX) {
            *encoding = ZIP_INT_8B;
        } else if (value >= INT16_MIN && value <= INT16_MAX) {
            *encoding = ZIP_INT_16B;
        } else if (value >= INT24_MIN && value <= INT24_MAX) {
            *encoding = ZIP_INT_24B;
        } else if (value >= INT32_MIN && value <= INT32_MAX) {
            *encoding = ZIP_INT_32B;
        } else {
            *encoding = ZIP_INT_64B;
        }
        *v = value;
        return 1;
    }
    return 0;
}

/* Store integer 'value' at 'p', encoded as 'encoding' */
void zipSaveInteger(unsigned char *p, int64_t value, unsigned char encoding) {
    int16_t i16;
    int32_t i32;
    int64_t i64;
    if (encoding == ZIP_INT_8B) {
        ((int8_t *) p)[0] = (int8_t) value;
    } else if (encoding == ZIP_INT_16B) {
        i16 = value;
        memcpy(p, &i16, sizeof(i16));
        memrev16ifbe(p);
    } else if (encoding == ZIP_INT_24B) {
        i32 = value << 8;
        memrev32ifbe(&i32);
        memcpy(p, ((uint8_t * ) & i32) + 1, sizeof(i32) - sizeof(uint8_t));
    } else if (encoding == ZIP_INT_32B) {
        i32 = value;
        memcpy(p, &i32, sizeof(i32));
        memrev32ifbe(p);
    } else if (encoding == ZIP_INT_64B) {
        i64 = value;
        memcpy(p, &i64, sizeof(i64));
        memrev64ifbe(p);
    } else if (encoding >= ZIP_INT_IMM_MIN && encoding <= ZIP_INT_IMM_MAX) {
        /* Nothing to do, the value is stored in the encoding itself. */
    } else {
        assert(NULL);
    }
}

/* Read integer encoded as 'encoding' from 'p' */
int64_t zipLoadInteger(unsigned char *p, unsigned char encoding) {
    int16_t i16;
    int32_t i32;
    int64_t i64, ret = 0;
    if (encoding == ZIP_INT_8B) {
        ret = ((int8_t *) p)[0];
    } else if (encoding == ZIP_INT_16B) {
        memcpy(&i16, p, sizeof(i16));
        memrev16ifbe(&i16);
        ret = i16;
    } else if (encoding == ZIP_INT_32B) {
        memcpy(&i32, p, sizeof(i32));
        memrev32ifbe(&i32);
        ret = i32;
    } else if (encoding == ZIP_INT_24B) {
        i32 = 0;
        memcpy(((uint8_t * ) & i32) + 1, p, sizeof(i32) - sizeof(uint8_t));
        memrev32ifbe(&i32);
        ret = i32 >> 8;
    } else if (encoding == ZIP_INT_64B) {
        memcpy(&i64, p, sizeof(i64));
        memrev64ifbe(&i64);
        ret = i64;
    } else if (encoding >= ZIP_INT_IMM_MIN && encoding <= ZIP_INT_IMM_MAX) {
        ret = (encoding & ZIP_INT_IMM_MASK) - 1;
    } else {
        assert(NULL);
    }
    return ret;
}

/* 把p指向的entry信息放入e */
void zipEntry(unsigned char *p, zlentry *e) {

    ZIP_DECODE_PREVLEN(p, e->prevrawlensize, e->prevrawlen);
    ZIP_DECODE_LENGTH(p + e->prevrawlensize, e->encoding, e->lensize, e->len);
    e->headersize = e->prevrawlensize + e->lensize;
    e->p = p;
}

/* 创建一个新的压缩列表 */
unsigned char *ziplistNew(void) {
    unsigned int bytes = ZIPLIST_HEADER_SIZE + ZIPLIST_END_SIZE; //头加尾占的字节数 zlbytes+zltail+zlend 4+4+2+1
    unsigned char *zl = zmalloc(bytes);
    ZIPLIST_BYTES(zl) = intrev32ifbe(bytes); //zlbytes赋值
    ZIPLIST_TAIL_OFFSET(zl) = intrev32ifbe(ZIPLIST_HEADER_SIZE); //zltail赋值
    ZIPLIST_LENGTH(zl) = 0; //给zllen赋值0
    zl[bytes - 1] = ZIP_END; //结束标志位
    return zl;
}

/* Resize the ziplist. */
unsigned char *ziplistResize(unsigned char *zl, size_t len) {
    assert(len < UINT32_MAX);
    zl = zrealloc(zl, len);
    ZIPLIST_BYTES(zl) = intrev32ifbe(len); //更新zlbytes
    zl[len - 1] = ZIP_END; //更新zlend
    return zl;
}

/* 当插入一个条目时，我们需要将下一个条目的 prevlen 字段设置为等于插入条目的长度。
 * 可能会出现该长度无法用 1 字节编码的情况，并且下一个条目需要变大一点以容纳 5 字节编码的 prevlen。
 * 这可以免费完成，因为这只在已经插入条目时发生（这会导致 realloc 和 memmove）。
 * 然而，对 prevlen 进行编码可能也需要增加该条目。 当存在大小接近 ZIP_BIG_PREVLEN 的连续条目时，
 * 这种效果可能会在整个 ziplist 中级联，因此我们需要检查 prevlen 是否可以在每个连续条目中进行编码。
 * 请注意，这种效果也可能反向发生，即编码 prevlen 字段所需的字节可能会缩小。
 * 故意忽略此效果，因为它可能会导致“抖动”效果，其中链 prevlen 字段首先增长，然后在连续插入后再次收缩。
 * 相反，允许该字段保持大于必要的大小，因为大的 prevlen 字段意味着 ziplist 无论如何都保存着大的条目。
 * 指针“p”指向不需要更新的第一个条目，即连续字段可能需要更新。
 *
 * 总的来说，级联更新。prev 1->5 需要处理。5->1不处理
 * */
unsigned char *__ziplistCascadeUpdate(unsigned char *zl, unsigned char *p) {
    size_t curlen = intrev32ifbe(ZIPLIST_BYTES(zl)), rawlen, rawlensize;
    size_t offset, noffset, extra;
    unsigned char *np;
    zlentry cur, next;

    while (p[0] != ZIP_END) {
        zipEntry(p, &cur);
        rawlen = cur.headersize + cur.len;
        rawlensize = zipStorePrevEntryLength(NULL, rawlen); //编码rawlen长度需要的字节数

        /* Abort if there is no next entry. */
        if (p[rawlen] == ZIP_END) break;
        zipEntry(p + rawlen, &next);

        /* Abort when "prevlen" has not changed. */
        if (next.prevrawlen == rawlen) break; //下一个记录前置entry编码长度的字节数没有变化,break

        if (next.prevrawlensize < rawlensize) {
            //后面的entry需要扩容
            /* The "prevlen" field of "next" needs more bytes to hold
             * the raw length of "cur". */
            offset = p - zl;
            extra = rawlensize - next.prevrawlensize; //1-5
            zl = ziplistResize(zl, curlen + extra);
            p = zl + offset;

            /* Current pointer and offset for next element. */
            np = p + rawlen;
            noffset = np - zl;

            /* Update tail offset when next element is not the tail element. */
            if ((zl + intrev32ifbe(ZIPLIST_TAIL_OFFSET(zl))) != np) {
                ZIPLIST_TAIL_OFFSET(zl) =
                        intrev32ifbe(intrev32ifbe(ZIPLIST_TAIL_OFFSET(zl)) + extra);
            }

            /* Move the tail to the back. */
            memmove(np + rawlensize,
                    np + next.prevrawlensize,
                    curlen - noffset - next.prevrawlensize - 1);
            zipStorePrevEntryLength(np, rawlen);

            /* Advance the cursor */
            p += rawlen;
            curlen += extra;
        } else {
            if (next.prevrawlensize > rawlensize) {
                /* This would result in shrinking, which we want to avoid.
                 * So, set "rawlen" in the available bytes. */
                zipStorePrevEntryLengthLarge(p + rawlen, rawlen);
            } else {
                zipStorePrevEntryLength(p + rawlen, rawlen);
            }

            /* Stop here, as the raw length of "next" has not changed. */
            break;
        }
    }
    return zl;
}

/* Delete "num" entries, starting at "p". Returns pointer to the ziplist. */
unsigned char *__ziplistDelete(unsigned char *zl, unsigned char *p, unsigned int num) {
    unsigned int i, totlen, deleted = 0;
    size_t offset;
    int nextdiff = 0;
    zlentry first, tail;
    zipEntry(p, &first);    //获取要删除的元素的首个节点
    for (i = 0; p[0] != ZIP_END && i < num; i++) {
        p += zipRawEntryLength(p); //计算要删除的元素占据的字节数
        deleted++;
    }

    totlen = p - first.p; /* 需要删除的字节 */
    if (totlen > 0) {
        if (p[0] != ZIP_END) {
            // 计算新的prevlen与旧的prevlen之间的字节数差
            nextdiff = zipPrevLenByteDiff(p, first.prevrawlen);

            // 如果有需要的话，将指针 p 后退 nextdiff 字节，为新 header 空出空间
            p -= nextdiff;
            // 将 first 的前置节点的长度编码至 p 中
            zipStorePrevEntryLength(p, first.prevrawlen);

            // 更新尾部节点的偏移量
            ZIPLIST_TAIL_OFFSET(zl) =
                    intrev32ifbe(intrev32ifbe(ZIPLIST_TAIL_OFFSET(zl)) - totlen);

            /* When the tail contains more than one entry, we need to take
             * "nextdiff" in account as well. Otherwise, a change in the
             * size of prevlen doesn't have an effect on the *tail* offset. */
            // 如果被删除节点之后，有多于一个节点
            // 那么程序需要将 nextdiff 记录的字节数也计算到表尾偏移量中
            // 这样才能让表尾偏移量正确对齐表尾节点
            zipEntry(p, &tail);
            if (p[tail.headersize + tail.len] != ZIP_END) {
                ZIPLIST_TAIL_OFFSET(zl) =
                        intrev32ifbe(intrev32ifbe(ZIPLIST_TAIL_OFFSET(zl)) + nextdiff);
            }

            // 将尾部移动到ziplist的前端
            memmove(first.p, p,
                    intrev32ifbe(ZIPLIST_BYTES(zl)) - (p - zl) - 1);
        } else {
            /* 执行到这里，说明删除的是zlend前的那个entry，不需要移动内存 */
            ZIPLIST_TAIL_OFFSET(zl) =
                    intrev32ifbe((first.p - zl) - first.prevrawlen);
        }

        /* Resize and update length */
        // 缩小并更新 ziplist 的长度
        offset = first.p - zl;
        zl = ziplistResize(zl, intrev32ifbe(ZIPLIST_BYTES(zl)) - totlen + nextdiff);
        ZIPLIST_INCR_LENGTH(zl, -deleted);
        p = zl + offset; //删除完毕后，更新p指向的位置

        /* When nextdiff != 0, the raw length of the next entry has changed, so
         * we need to cascade the update throughout the ziplist */
        // 如果 p 所指向的节点的大小已经变更，那么进行级联更新
        // 检查 p 之后的所有节点是否符合 ziplist 的编码要求
        // T = O(N^2)
        if (nextdiff != 0)
            zl = __ziplistCascadeUpdate(zl, p);
    }
    return zl;
}

/* Insert item at "p". */
unsigned char *__ziplistInsert(unsigned char *zl, unsigned char *p, unsigned char *s, unsigned int slen) {
    size_t curlen = intrev32ifbe(ZIPLIST_BYTES(zl)), reqlen;
    unsigned int prevlensize, prevlen = 0;
    size_t offset;
    int nextdiff = 0;
    unsigned char encoding = 0;
    long long value = 123456789; /* initialized to avoid warning. Using a value
                                    that is easy to see if for some reason
                                    we use it uninitialized. */
    zlentry tail;

    /* Find out prevlen for the entry that is inserted. */
    if (p[0] != ZIP_END) {
        ZIP_DECODE_PREVLEN(p, prevlensize, prevlen);
    } else {
        unsigned char *ptail = ZIPLIST_ENTRY_TAIL(zl);
        if (ptail[0] != ZIP_END) {
            prevlen = zipRawEntryLength(ptail);
        }
    }

    /* See if the entry can be encoded */
    //尝试转换成整型,使用整型编码,
    //reqlen保存节点值的长度
    if (zipTryEncoding(s, slen, &value, &encoding)) {
        /* 'encoding' is set to the appropriate integer encoding */
        reqlen = zipIntSize(encoding);
    } else {
        /* 'encoding' 保持不变，但是 zipStoreEntryEncoding 将使用
        * 字符串长度以确定如何对其进行编码。 */
        reqlen = slen;
    }
    //加上编码前置节点需要的长度
    reqlen += zipStorePrevEntryLength(NULL, prevlen);
    //加上编码当前节点所需的长度
    reqlen += zipStoreEntryEncoding(NULL, encoding, slen);

    /* 当插入位置不等于尾部时，我们需要确保下一个条目可以在其 prevlen 字段中保存该条目的长度。 */
    int forcelarge = 0;
    nextdiff = (p[0] != ZIP_END) ? zipPrevLenByteDiff(p, reqlen) : 0;
    if (nextdiff == -4 && reqlen < 4) {
        //只管扩大,缩小的情况不管
        nextdiff = 0;
        forcelarge = 1;
    }

    /* Store offset because a realloc may change the address of zl. */
    offset = p - zl; //offset是从zl起始到p的偏移量
    zl = ziplistResize(zl, curlen + reqlen + nextdiff);
    p = zl + offset; //p指向要被插入的节点后

    /* Apply memory move when necessary and update tail offset. */
    if (p[0] != ZIP_END) {
        /* Subtract one because of the ZIP_END bytes */
        /*
         * memmove(*dest, *src, size_t len)
         * 为新插入的元素腾出空间.
         * curlen:当前长度;
         * offset相当于从zl起始到第一个entry的偏移;
         * 1是zlend;
         * nextdiff是可能存在的prev_entry_length的变化
         * */
        memmove(p + reqlen, p - nextdiff, curlen - offset - 1 + nextdiff);

        /* Encode this entry's raw length in the next entry. */
        if (forcelarge)
            zipStorePrevEntryLengthLarge(p + reqlen, reqlen);
        else
            zipStorePrevEntryLength(p + reqlen, reqlen);

        /* Update offset for tail */
        ZIPLIST_TAIL_OFFSET(zl) =
                intrev32ifbe(intrev32ifbe(ZIPLIST_TAIL_OFFSET(zl)) + reqlen);

        /* When the tail contains more than one entry, we need to take
         * "nextdiff" in account as well. Otherwise, a change in the
         * size of prevlen doesn't have an effect on the *tail* offset. */
        zipEntry(p + reqlen, &tail);
        if (p[reqlen + tail.headersize + tail.len] != ZIP_END) {
            ZIPLIST_TAIL_OFFSET(zl) =
                    intrev32ifbe(intrev32ifbe(ZIPLIST_TAIL_OFFSET(zl)) + nextdiff);
        }
    } else {
        /* This element will be the new tail. */
        ZIPLIST_TAIL_OFFSET(zl) = intrev32ifbe(p - zl);
    }

    /* When nextdiff != 0, the raw length of the next entry has changed, so
     * we need to cascade the update throughout the ziplist
     * 级联更新
     * */
    if (nextdiff != 0) {
        offset = p - zl;
        zl = __ziplistCascadeUpdate(zl, p + reqlen); //上面已经插入新节点完事了, 所以p + reqlen就是指向原来的entry的指针
        p = zl + offset;
    }

    /* Write the entry */
    p += zipStorePrevEntryLength(p, prevlen); //保存perv_len
    p += zipStoreEntryEncoding(p, encoding, slen); //保存encoding
    if (ZIP_IS_STR(encoding)) {
        memcpy(p, s, slen); //保存string类型的content
    } else {
        zipSaveInteger(p, value, encoding);
    }
    ZIPLIST_INCR_LENGTH(zl, 1);//更新zllen
    return zl;
}

/* Merge ziplists 'first' and 'second' by appending 'second' to 'first'.
 *
 * NOTE: The larger ziplist is reallocated to contain the new merged ziplist.
 * Either 'first' or 'second' can be used for the result.  The parameter not
 * used will be free'd and set to NULL.
 *
 * After calling this function, the input parameters are no longer valid since
 * they are changed and free'd in-place.
 *
 * The result ziplist is the contents of 'first' followed by 'second'.
 *
 * On failure: returns NULL if the merge is impossible.
 * On success: returns the merged ziplist (which is expanded version of either
 * 'first' or 'second', also frees the other unused input ziplist, and sets the
 * input ziplist argument equal to newly reallocated ziplist return value. */
unsigned char *ziplistMerge(unsigned char **first, unsigned char **second) {
    /* If any params are null, we can't merge, so NULL. */
    if (first == NULL || *first == NULL || second == NULL || *second == NULL)
        return NULL;

    /* Can't merge same list into itself. */
    if (*first == *second)
        return NULL;

    size_t first_bytes = intrev32ifbe(ZIPLIST_BYTES(*first));
    size_t first_len = intrev16ifbe(ZIPLIST_LENGTH(*first));

    size_t second_bytes = intrev32ifbe(ZIPLIST_BYTES(*second));
    size_t second_len = intrev16ifbe(ZIPLIST_LENGTH(*second));

    int append;
    unsigned char *source, *target;
    size_t target_bytes, source_bytes;
    /* Pick the largest ziplist so we can resize easily in-place.
     * We must also track if we are now appending or prepending to
     * the target ziplist. */
    if (first_len >= second_len) {
        /* retain first, append second to first. */
        target = *first;
        target_bytes = first_bytes;
        source = *second;
        source_bytes = second_bytes;
        append = 1;
    } else {
        /* else, retain second, prepend first to second. */
        target = *second;
        target_bytes = second_bytes;
        source = *first;
        source_bytes = first_bytes;
        append = 0;
    }

    /* Calculate final bytes (subtract one pair of metadata) */
    size_t zlbytes = first_bytes + second_bytes -
                     ZIPLIST_HEADER_SIZE - ZIPLIST_END_SIZE;
    size_t zllength = first_len + second_len;

    /* Combined zl length should be limited within UINT16_MAX */
    zllength = zllength < UINT16_MAX ? zllength : UINT16_MAX;

    /* larger values can't be stored into ZIPLIST_BYTES */
    assert(zlbytes < UINT32_MAX);

    /* Save offset positions before we start ripping memory apart. */
    size_t first_offset = intrev32ifbe(ZIPLIST_TAIL_OFFSET(*first));
    size_t second_offset = intrev32ifbe(ZIPLIST_TAIL_OFFSET(*second));

    /* Extend target to new zlbytes then append or prepend source. */
    target = zrealloc(target, zlbytes);
    if (append) {
        /* append == appending to target */
        /* Copy source after target (copying over original [END]):
         *   [TARGET - END, SOURCE - HEADER] */
        memcpy(target + target_bytes - ZIPLIST_END_SIZE,
               source + ZIPLIST_HEADER_SIZE,
               source_bytes - ZIPLIST_HEADER_SIZE);
    } else {
        /* !append == prepending to target */
        /* Move target *contents* exactly size of (source - [END]),
         * then copy source into vacataed space (source - [END]):
         *   [SOURCE - END, TARGET - HEADER] */
        memmove(target + source_bytes - ZIPLIST_END_SIZE,
                target + ZIPLIST_HEADER_SIZE,
                target_bytes - ZIPLIST_HEADER_SIZE);
        memcpy(target, source, source_bytes - ZIPLIST_END_SIZE);
    }

    /* Update header metadata. */
    ZIPLIST_BYTES(target) = intrev32ifbe(zlbytes);
    ZIPLIST_LENGTH(target) = intrev16ifbe(zllength);
    /* New tail offset is:
     *   + N bytes of first ziplist
     *   - 1 byte for [END] of first ziplist
     *   + M bytes for the offset of the original tail of the second ziplist
     *   - J bytes for HEADER because second_offset keeps no header. */
    ZIPLIST_TAIL_OFFSET(target) = intrev32ifbe(
            (first_bytes - ZIPLIST_END_SIZE) +
            (second_offset - ZIPLIST_HEADER_SIZE));

    /* __ziplistCascadeUpdate just fixes the prev length values until it finds a
     * correct prev length value (then it assumes the rest of the list is okay).
     * We tell CascadeUpdate to start at the first ziplist's tail element to fix
     * the merge seam. */
    target = __ziplistCascadeUpdate(target, target + first_offset);

    /* Now free and NULL out what we didn't realloc */
    if (append) {
        zfree(*second);
        *second = NULL;
        *first = target;
    } else {
        zfree(*first);
        *first = NULL;
        *second = target;
    }
    return target;
}

unsigned char *ziplistPush(unsigned char *zl, unsigned char *s, unsigned int slen, int where) {
    /**
     * s：指向要插入或推入的数据的指针，即要添加到压缩列表中的数据。
     * slen：要插入或推入的数据的长度。
     * */
    unsigned char *p;
    p = (where == ZIPLIST_HEAD) ? ZIPLIST_ENTRY_HEAD(zl) : ZIPLIST_ENTRY_END(zl); //得到插入位置
    return __ziplistInsert(zl, p, s, slen);
}

/* 返回给定索引上的节点。 当给定索引为负数时，列表将从后向前遍历。
 * 当列表在提供的索引处不包含元素时，返回 NULL。
 * O(N)
 * */
unsigned char *ziplistIndex(unsigned char *zl, int index) {
    unsigned char *p;
    unsigned int prevlensize, prevlen = 0;
    if (index < 0) {
        index = (-index) - 1;
        p = ZIPLIST_ENTRY_TAIL(zl); //获取zltail指向的位置
        if (p[0] != ZIP_END) { //不为空
            ZIP_DECODE_PREVLEN(p, prevlensize, prevlen);
            while (prevlen > 0 && index--) {
                p -= prevlen; //指针前移,指向前一个entry开始位置
                ZIP_DECODE_PREVLEN(p, prevlensize, prevlen);
            }
        }
    } else {
        p = ZIPLIST_ENTRY_HEAD(zl); //正向,指向第一个entry结构体的起始位置
        while (p[0] != ZIP_END && index--) {
            p += zipRawEntryLength(p); //指针移动到下一个entry开始位置
        }
    }
    return (p[0] == ZIP_END || index > 0) ? NULL : p; //返回第index个entry的指针
}

/* 返回指向 ziplist 中下一个entry的指针。
 * zl 是指向 ziplist 的指针，p 是指向当前元素的指针，
 * 返回 'p' 之后的元素，如果到达末尾则返回 NULL。*/
unsigned char *ziplistNext(unsigned char *zl, unsigned char *p) {
    ((void) zl);

    /* “p”可能等于 ZIP_END，这是由 ziplistDelete 引起的，我们应该返回 NULL。
     * 否则，当 *next* 元素为 ZIP_END（没有下一个entry）时，我们应该返回 NULL。 */
    if (p[0] == ZIP_END) {
        return NULL;
    }

    p += zipRawEntryLength(p);
    if (p[0] == ZIP_END) {
        return NULL;
    }

    return p;
}

/* Return pointer to previous entry in ziplist. */
unsigned char *ziplistPrev(unsigned char *zl, unsigned char *p) {
    unsigned int prevlensize, prevlen = 0;

    /* Iterating backwards from ZIP_END should return the tail. When "p" is
     * equal to the first element of the list, we're already at the head,
     * and should return NULL. */
    if (p[0] == ZIP_END) {
        p = ZIPLIST_ENTRY_TAIL(zl); //将指针 p 移动到压缩列表的尾部entry
        return (p[0] == ZIP_END) ? NULL : p;
    } else if (p == ZIPLIST_ENTRY_HEAD(zl)) {
        //和当前ziplist的第一个entry比较,如果是第一个,那么肯定没有前置节点
        return NULL;
    } else {
        ZIP_DECODE_PREVLEN(p, prevlensize, prevlen); // 解码当前元素的前一个元素长度
        assert(prevlen > 0);
        return p - prevlen; //将指针 p 向前移动 prevlen 个字节，即移到前一个元素的位置。
    }
}

/* Get entry pointed to by 'p' and store in either '*sstr' or 'sval' depending
 * on the encoding of the entry. '*sstr' is always set to NULL to be able
 * to find out whether the string pointer or the integer value was set.
 * Return 0 if 'p' points to the end of the ziplist, 1 otherwise.
 *
 * p：当前元素的地址。
 * sstr：指针的指针，用于保存字符串数据的地址。
 * slen：整数的指针，用于保存字符串数据的长度。
 * sval：长整型数的指针，用于保存整数数据的值。
 * */
unsigned int ziplistGet(unsigned char *p, unsigned char **sstr, unsigned int *slen, long long *sval) {
    zlentry entry;
    if (p == NULL || p[0] == ZIP_END) return 0;
    if (sstr) *sstr = NULL;

    zipEntry(p, &entry);
    if (ZIP_IS_STR(entry.encoding)) {
        if (sstr) {
            *slen = entry.len;
            *sstr = p + entry.headersize;
        }
    } else {
        if (sval) {
            *sval = zipLoadInteger(p + entry.headersize, entry.encoding);
        }
    }
    return 1;
}

//在zl的p插入slen长度的s
unsigned char *ziplistInsert(unsigned char *zl, unsigned char *p, unsigned char *s, unsigned int slen) {
    return __ziplistInsert(zl, p, s, slen);
}

/* 从 ziplist 中删除 *p 指向的单个条目。同时更新 *p，以便能够在删除条目时迭代 ziplist。
 * 平均O(N)，最坏O(N²)
 * */
unsigned char *ziplistDelete(unsigned char *zl, unsigned char **p) {
    size_t offset = *p - zl;
    zl = __ziplistDelete(zl, *p, 1);

    /* 将指向当前元素的指针存储在 p 中，因为 ziplistDelete 将执行重新分配，
     * 这可能会导致不同的“zl”指针。 当删除方向是从后到前时，
     * 我们可能会删除最后一个条目并最终得到“p”指向 ZIP_END 的结果，因此请检查这一点。 */
    *p = zl + offset;
    return zl;
}

/* 删除在给定范围的节点，存在级联更新 */
unsigned char *ziplistDeleteRange(unsigned char *zl, int index, unsigned int num) {
    unsigned char *p = ziplistIndex(zl, index);
    return (p == NULL) ? zl : __ziplistDelete(zl, p, num);
}

/* Compare entry pointer to by 'p' with 'sstr' of length 'slen'. */
/* Return 1 if equal. */
unsigned int ziplistCompare(unsigned char *p, unsigned char *sstr, unsigned int slen) {
    zlentry entry;
    unsigned char sencoding;
    long long zval, sval;
    if (p[0] == ZIP_END) return 0;

    zipEntry(p, &entry);
    if (ZIP_IS_STR(entry.encoding)) {
        /* Raw compare */
        if (entry.len == slen) {
            return memcmp(p + entry.headersize, sstr, slen) == 0;
        } else {
            return 0;
        }
    } else {
        /* Try to compare encoded values. Don't compare encoding because
         * different implementations may encoded integers differently. */
        if (zipTryEncoding(sstr, slen, &sval, &sencoding)) {
            zval = zipLoadInteger(p + entry.headersize, entry.encoding);
            return zval == sval;
        }
    }
    return 0;
}

/* 在压缩列表中查找并返回包含了给定值的节点
 * p：传入一个指向 ziplist 起始位置的 unsigned char 指针，表示要开始查找的位置。
  vstr：传入一个指向要查找的值的 unsigned char 指针，表示要查找的具体值。
  vlen：传入一个 unsigned int 类型的整数，表示要查找的值的长度。
  skip：传入一个 unsigned int 类型的整数，表示每次查找时要跳过的条目数。
 * */
unsigned char *ziplistFind(unsigned char *p, unsigned char *vstr, unsigned int vlen, unsigned int skip) {
    int skipcnt = 0;
    unsigned char vencoding = 0;
    long long vll = 0;

    while (p[0] != ZIP_END) {
        unsigned int prevlensize, encoding, lensize, len;
        unsigned char *q;

        ZIP_DECODE_PREVLENSIZE(p, prevlensize); // 解码前置节点长度所占字节数
        ZIP_DECODE_LENGTH(p + prevlensize, encoding, lensize, len);// 解码当前节点的编码方式、节点长度所占字节数和节点长度
        q = p + prevlensize + lensize; //指向content

        if (skipcnt == 0) {
            /* Compare current entry with specified entry */
            if (ZIP_IS_STR(encoding)) {
                //字符串，memcmp相等时返回0
                if (len == vlen && memcmp(q, vstr, vlen) == 0) {
                    return p;
                }
            } else {
                /* 查明搜索字段是否可以编码。
                 * 只在第一次执行此操作，一旦完成，编码就会设置为非零，并且所有内容都会设置为整数值。*/
                if (vencoding == 0) {
                    if (!zipTryEncoding(vstr, vlen, &vll, &vencoding)) {
                        /* If the entry can't be encoded we set it to
                         * UCHAR_MAX so that we don't retry again the next
                         * time. */
                        vencoding = UCHAR_MAX;
                    }
                    /* Must be non-zero by now */
                    assert(vencoding);
                }

                /* Compare current entry with specified entry, do it only
                 * if vencoding != UCHAR_MAX because if there is no encoding
                 * possible for the field it can't be a valid integer. */
                if (vencoding != UCHAR_MAX) {
                    long long ll = zipLoadInteger(q, encoding); // 加载entry的整数值
                    if (ll == vll) {
                        return p;
                    }
                }
            }

            /* Reset skip count */
            skipcnt = skip;
        } else {
            /* Skip entry */
            skipcnt--;
        }

        /* // 移动到下一个entry的起始位置*/
        p = q + len;
    }

    return NULL;
}

/*  * 返回 ziplist 中的节点个数
 *
 * T = O(N)
 * */
unsigned int ziplistLen(unsigned char *zl) {
    unsigned int len = 0;
    //如果节点数小于UINT16_MAX,
    //
    // T=O(1)
    if (intrev16ifbe(ZIPLIST_LENGTH(zl)) < UINT16_MAX) {
        len = intrev16ifbe(ZIPLIST_LENGTH(zl));
    } else {
        //一个一个遍历,获得节点数
        unsigned char *p = zl + ZIPLIST_HEADER_SIZE;
        while (*p != ZIP_END) {
            p += zipRawEntryLength(p);
            len++;
        }

        /* Re-store length if small enough */
        if (len < UINT16_MAX) ZIPLIST_LENGTH(zl) = intrev16ifbe(len);
    }
    return len;
}

/* 返回压缩列表目前占用的字节数 */
size_t ziplistBlobLen(unsigned char *zl) {
    return intrev32ifbe(ZIPLIST_BYTES(zl));
}

void ziplistRepr(unsigned char *zl) {
    unsigned char *p;
    int index = 0;
    zlentry entry;

    printf(
            "{total bytes %d} "
            "{num entries %u}\n"
            "{tail offset %u}\n",
            intrev32ifbe(ZIPLIST_BYTES(zl)),
            intrev16ifbe(ZIPLIST_LENGTH(zl)),
            intrev32ifbe(ZIPLIST_TAIL_OFFSET(zl)));
    p = ZIPLIST_ENTRY_HEAD(zl);
    while (*p != ZIP_END) {
        zipEntry(p, &entry);
        printf(
                "{\n"
                "\taddr 0x%08lx,\n"
                "\tindex %2d,\n"
                "\toffset %5ld,\n"
                "\thdr+entry len: %5u,\n"
                "\thdr len%2u,\n"
                "\tprevrawlen: %5u,\n"
                "\tprevrawlensize: %2u,\n"
                "\tpayload %5u\n",
                (long unsigned) p,
                index,
                (unsigned long) (p - zl),
                entry.headersize + entry.len,
                entry.headersize,
                entry.prevrawlen,
                entry.prevrawlensize,
                entry.len);
        printf("\tbytes: ");
        for (unsigned int i = 0; i < entry.headersize + entry.len; i++) {
            printf("%02x|", p[i]);
        }
        printf("\n");
        p += entry.headersize;
        if (ZIP_IS_STR(entry.encoding)) {
            printf("\t[str]");
            if (entry.len > 40) {
                if (fwrite(p, 40, 1, stdout) == 0) perror("fwrite");
                printf("...");
            } else {
                if (entry.len &&
                    fwrite(p, entry.len, 1, stdout) == 0)
                    perror("fwrite");
            }
        } else {
            printf("\t[int]%lld", (long long) zipLoadInteger(p, entry.encoding));
        }
        printf("\n}\n");
        p += entry.len;
        index++;
    }
    printf("{end}\n\n");
}

#ifdef REDIS_TEST
#include <sys/time.h>
#include "adlist.h"
#include "sds.h"

#define debug(f, ...) { if (DEBUG) printf(f, __VA_ARGS__); }

static unsigned char *createList() {
    unsigned char *zl = ziplistNew();
    zl = ziplistPush(zl, (unsigned char*)"foo", 3, ZIPLIST_TAIL);
    zl = ziplistPush(zl, (unsigned char*)"quux", 4, ZIPLIST_TAIL);
    zl = ziplistPush(zl, (unsigned char*)"hello", 5, ZIPLIST_HEAD);
    zl = ziplistPush(zl, (unsigned char*)"1024", 4, ZIPLIST_TAIL);
    return zl;
}

static unsigned char *createIntList() {
    unsigned char *zl = ziplistNew();
    char buf[32];

    sprintf(buf, "100");
    zl = ziplistPush(zl, (unsigned char*)buf, strlen(buf), ZIPLIST_TAIL);
    sprintf(buf, "128000");
    zl = ziplistPush(zl, (unsigned char*)buf, strlen(buf), ZIPLIST_TAIL);
    sprintf(buf, "-100");
    zl = ziplistPush(zl, (unsigned char*)buf, strlen(buf), ZIPLIST_HEAD);
    sprintf(buf, "4294967296");
    zl = ziplistPush(zl, (unsigned char*)buf, strlen(buf), ZIPLIST_HEAD);
    sprintf(buf, "non integer");
    zl = ziplistPush(zl, (unsigned char*)buf, strlen(buf), ZIPLIST_TAIL);
    sprintf(buf, "much much longer non integer");
    zl = ziplistPush(zl, (unsigned char*)buf, strlen(buf), ZIPLIST_TAIL);
    return zl;
}

static long long usec(void) {
    struct timeval tv;
    gettimeofday(&tv,NULL);
    return (((long long)tv.tv_sec)*1000000)+tv.tv_usec;
}

static void stress(int pos, int num, int maxsize, int dnum) {
    int i,j,k;
    unsigned char *zl;
    char posstr[2][5] = { "HEAD", "TAIL" };
    long long start;
    for (i = 0; i < maxsize; i+=dnum) {
        zl = ziplistNew();
        for (j = 0; j < i; j++) {
            zl = ziplistPush(zl,(unsigned char*)"quux",4,ZIPLIST_TAIL);
        }

        /* Do num times a push+pop from pos */
        start = usec();
        for (k = 0; k < num; k++) {
            zl = ziplistPush(zl,(unsigned char*)"quux",4,pos);
            zl = ziplistDeleteRange(zl,0,1);
        }
        printf("List size: %8d, bytes: %8d, %dx push+pop (%s): %6lld usec\n",
            i,intrev32ifbe(ZIPLIST_BYTES(zl)),num,posstr[pos],usec()-start);
        zfree(zl);
    }
}

static unsigned char *pop(unsigned char *zl, int where) {
    unsigned char *p, *vstr;
    unsigned int vlen;
    long long vlong;

    p = ziplistIndex(zl,where == ZIPLIST_HEAD ? 0 : -1);
    if (ziplistGet(p,&vstr,&vlen,&vlong)) {
        if (where == ZIPLIST_HEAD)
            printf("Pop head: ");
        else
            printf("Pop tail: ");

        if (vstr) {
            if (vlen && fwrite(vstr,vlen,1,stdout) == 0) perror("fwrite");
        }
        else {
            printf("%lld", vlong);
        }

        printf("\n");
        return ziplistDelete(zl,&p);
    } else {
        printf("ERROR: Could not pop\n");
        exit(1);
    }
}

static int randstring(char *target, unsigned int min, unsigned int max) {
    int p = 0;
    int len = min+rand()%(max-min+1);
    int minval, maxval;
    switch(rand() % 3) {
    case 0:
        minval = 0;
        maxval = 255;
    break;
    case 1:
        minval = 48;
        maxval = 122;
    break;
    case 2:
        minval = 48;
        maxval = 52;
    break;
    default:
        assert(NULL);
    }

    while(p < len)
        target[p++] = minval+rand()%(maxval-minval+1);
    return len;
}

static void verify(unsigned char *zl, zlentry *e) {
    int len = ziplistLen(zl);
    zlentry _e;

    ZIPLIST_ENTRY_ZERO(&_e);

    for (int i = 0; i < len; i++) {
        memset(&e[i], 0, sizeof(zlentry));
        zipEntry(ziplistIndex(zl, i), &e[i]);

        memset(&_e, 0, sizeof(zlentry));
        zipEntry(ziplistIndex(zl, -len+i), &_e);

        assert(memcmp(&e[i], &_e, sizeof(zlentry)) == 0);
    }
}

int ziplistTest(int argc, char **argv) {
    unsigned char *zl, *p;
    unsigned char *entry;
    unsigned int elen;
    long long value;

    /* If an argument is given, use it as the random seed. */
    if (argc == 2)
        srand(atoi(argv[1]));

    zl = createIntList();
    ziplistRepr(zl);

    zfree(zl);

    zl = createList();
    ziplistRepr(zl);

    zl = pop(zl,ZIPLIST_TAIL);
    ziplistRepr(zl);

    zl = pop(zl,ZIPLIST_HEAD);
    ziplistRepr(zl);

    zl = pop(zl,ZIPLIST_TAIL);
    ziplistRepr(zl);

    zl = pop(zl,ZIPLIST_TAIL);
    ziplistRepr(zl);

    zfree(zl);

    printf("Get element at index 3:\n");
    {
        zl = createList();
        p = ziplistIndex(zl, 3);
        if (!ziplistGet(p, &entry, &elen, &value)) {
            printf("ERROR: Could not access index 3\n");
            return 1;
        }
        if (entry) {
            if (elen && fwrite(entry,elen,1,stdout) == 0) perror("fwrite");
            printf("\n");
        } else {
            printf("%lld\n", value);
        }
        printf("\n");
        zfree(zl);
    }

    printf("Get element at index 4 (out of range):\n");
    {
        zl = createList();
        p = ziplistIndex(zl, 4);
        if (p == NULL) {
            printf("No entry\n");
        } else {
            printf("ERROR: Out of range index should return NULL, returned offset: %ld\n", p-zl);
            return 1;
        }
        printf("\n");
        zfree(zl);
    }

    printf("Get element at index -1 (last element):\n");
    {
        zl = createList();
        p = ziplistIndex(zl, -1);
        if (!ziplistGet(p, &entry, &elen, &value)) {
            printf("ERROR: Could not access index -1\n");
            return 1;
        }
        if (entry) {
            if (elen && fwrite(entry,elen,1,stdout) == 0) perror("fwrite");
            printf("\n");
        } else {
            printf("%lld\n", value);
        }
        printf("\n");
        zfree(zl);
    }

    printf("Get element at index -4 (first element):\n");
    {
        zl = createList();
        p = ziplistIndex(zl, -4);
        if (!ziplistGet(p, &entry, &elen, &value)) {
            printf("ERROR: Could not access index -4\n");
            return 1;
        }
        if (entry) {
            if (elen && fwrite(entry,elen,1,stdout) == 0) perror("fwrite");
            printf("\n");
        } else {
            printf("%lld\n", value);
        }
        printf("\n");
        zfree(zl);
    }

    printf("Get element at index -5 (reverse out of range):\n");
    {
        zl = createList();
        p = ziplistIndex(zl, -5);
        if (p == NULL) {
            printf("No entry\n");
        } else {
            printf("ERROR: Out of range index should return NULL, returned offset: %ld\n", p-zl);
            return 1;
        }
        printf("\n");
        zfree(zl);
    }

    printf("Iterate list from 0 to end:\n");
    {
        zl = createList();
        p = ziplistIndex(zl, 0);
        while (ziplistGet(p, &entry, &elen, &value)) {
            printf("Entry: ");
            if (entry) {
                if (elen && fwrite(entry,elen,1,stdout) == 0) perror("fwrite");
            } else {
                printf("%lld", value);
            }
            p = ziplistNext(zl,p);
            printf("\n");
        }
        printf("\n");
        zfree(zl);
    }

    printf("Iterate list from 1 to end:\n");
    {
        zl = createList();
        p = ziplistIndex(zl, 1);
        while (ziplistGet(p, &entry, &elen, &value)) {
            printf("Entry: ");
            if (entry) {
                if (elen && fwrite(entry,elen,1,stdout) == 0) perror("fwrite");
            } else {
                printf("%lld", value);
            }
            p = ziplistNext(zl,p);
            printf("\n");
        }
        printf("\n");
        zfree(zl);
    }

    printf("Iterate list from 2 to end:\n");
    {
        zl = createList();
        p = ziplistIndex(zl, 2);
        while (ziplistGet(p, &entry, &elen, &value)) {
            printf("Entry: ");
            if (entry) {
                if (elen && fwrite(entry,elen,1,stdout) == 0) perror("fwrite");
            } else {
                printf("%lld", value);
            }
            p = ziplistNext(zl,p);
            printf("\n");
        }
        printf("\n");
        zfree(zl);
    }

    printf("Iterate starting out of range:\n");
    {
        zl = createList();
        p = ziplistIndex(zl, 4);
        if (!ziplistGet(p, &entry, &elen, &value)) {
            printf("No entry\n");
        } else {
            printf("ERROR\n");
        }
        printf("\n");
        zfree(zl);
    }

    printf("Iterate from back to front:\n");
    {
        zl = createList();
        p = ziplistIndex(zl, -1);
        while (ziplistGet(p, &entry, &elen, &value)) {
            printf("Entry: ");
            if (entry) {
                if (elen && fwrite(entry,elen,1,stdout) == 0) perror("fwrite");
            } else {
                printf("%lld", value);
            }
            p = ziplistPrev(zl,p);
            printf("\n");
        }
        printf("\n");
        zfree(zl);
    }

    printf("Iterate from back to front, deleting all items:\n");
    {
        zl = createList();
        p = ziplistIndex(zl, -1);
        while (ziplistGet(p, &entry, &elen, &value)) {
            printf("Entry: ");
            if (entry) {
                if (elen && fwrite(entry,elen,1,stdout) == 0) perror("fwrite");
            } else {
                printf("%lld", value);
            }
            zl = ziplistDelete(zl,&p);
            p = ziplistPrev(zl,p);
            printf("\n");
        }
        printf("\n");
        zfree(zl);
    }

    printf("Delete inclusive range 0,0:\n");
    {
        zl = createList();
        zl = ziplistDeleteRange(zl, 0, 1);
        ziplistRepr(zl);
        zfree(zl);
    }

    printf("Delete inclusive range 0,1:\n");
    {
        zl = createList();
        zl = ziplistDeleteRange(zl, 0, 2);
        ziplistRepr(zl);
        zfree(zl);
    }

    printf("Delete inclusive range 1,2:\n");
    {
        zl = createList();
        zl = ziplistDeleteRange(zl, 1, 2);
        ziplistRepr(zl);
        zfree(zl);
    }

    printf("Delete with start index out of range:\n");
    {
        zl = createList();
        zl = ziplistDeleteRange(zl, 5, 1);
        ziplistRepr(zl);
        zfree(zl);
    }

    printf("Delete with num overflow:\n");
    {
        zl = createList();
        zl = ziplistDeleteRange(zl, 1, 5);
        ziplistRepr(zl);
        zfree(zl);
    }

    printf("Delete foo while iterating:\n");
    {
        zl = createList();
        p = ziplistIndex(zl,0);
        while (ziplistGet(p,&entry,&elen,&value)) {
            if (entry && strncmp("foo",(char*)entry,elen) == 0) {
                printf("Delete foo\n");
                zl = ziplistDelete(zl,&p);
            } else {
                printf("Entry: ");
                if (entry) {
                    if (elen && fwrite(entry,elen,1,stdout) == 0)
                        perror("fwrite");
                } else {
                    printf("%lld",value);
                }
                p = ziplistNext(zl,p);
                printf("\n");
            }
        }
        printf("\n");
        ziplistRepr(zl);
        zfree(zl);
    }

    printf("Regression test for >255 byte strings:\n");
    {
        char v1[257] = {0}, v2[257] = {0};
        memset(v1,'x',256);
        memset(v2,'y',256);
        zl = ziplistNew();
        zl = ziplistPush(zl,(unsigned char*)v1,strlen(v1),ZIPLIST_TAIL);
        zl = ziplistPush(zl,(unsigned char*)v2,strlen(v2),ZIPLIST_TAIL);

        /* Pop values again and compare their value. */
        p = ziplistIndex(zl,0);
        assert(ziplistGet(p,&entry,&elen,&value));
        assert(strncmp(v1,(char*)entry,elen) == 0);
        p = ziplistIndex(zl,1);
        assert(ziplistGet(p,&entry,&elen,&value));
        assert(strncmp(v2,(char*)entry,elen) == 0);
        printf("SUCCESS\n\n");
        zfree(zl);
    }

    printf("Regression test deleting next to last entries:\n");
    {
        char v[3][257] = {{0}};
        zlentry e[3] = {{.prevrawlensize = 0, .prevrawlen = 0, .lensize = 0,
                         .len = 0, .headersize = 0, .encoding = 0, .p = NULL}};
        size_t i;

        for (i = 0; i < (sizeof(v)/sizeof(v[0])); i++) {
            memset(v[i], 'a' + i, sizeof(v[0]));
        }

        v[0][256] = '\0';
        v[1][  1] = '\0';
        v[2][256] = '\0';

        zl = ziplistNew();
        for (i = 0; i < (sizeof(v)/sizeof(v[0])); i++) {
            zl = ziplistPush(zl, (unsigned char *) v[i], strlen(v[i]), ZIPLIST_TAIL);
        }

        verify(zl, e);

        assert(e[0].prevrawlensize == 1);
        assert(e[1].prevrawlensize == 5);
        assert(e[2].prevrawlensize == 1);

        /* Deleting entry 1 will increase `prevrawlensize` for entry 2 */
        unsigned char *p = e[1].p;
        zl = ziplistDelete(zl, &p);

        verify(zl, e);

        assert(e[0].prevrawlensize == 1);
        assert(e[1].prevrawlensize == 5);

        printf("SUCCESS\n\n");
        zfree(zl);
    }

    printf("Create long list and check indices:\n");
    {
        zl = ziplistNew();
        char buf[32];
        int i,len;
        for (i = 0; i < 1000; i++) {
            len = sprintf(buf,"%d",i);
            zl = ziplistPush(zl,(unsigned char*)buf,len,ZIPLIST_TAIL);
        }
        for (i = 0; i < 1000; i++) {
            p = ziplistIndex(zl,i);
            assert(ziplistGet(p,NULL,NULL,&value));
            assert(i == value);

            p = ziplistIndex(zl,-i-1);
            assert(ziplistGet(p,NULL,NULL,&value));
            assert(999-i == value);
        }
        printf("SUCCESS\n\n");
        zfree(zl);
    }

    printf("Compare strings with ziplist entries:\n");
    {
        zl = createList();
        p = ziplistIndex(zl,0);
        if (!ziplistCompare(p,(unsigned char*)"hello",5)) {
            printf("ERROR: not \"hello\"\n");
            return 1;
        }
        if (ziplistCompare(p,(unsigned char*)"hella",5)) {
            printf("ERROR: \"hella\"\n");
            return 1;
        }

        p = ziplistIndex(zl,3);
        if (!ziplistCompare(p,(unsigned char*)"1024",4)) {
            printf("ERROR: not \"1024\"\n");
            return 1;
        }
        if (ziplistCompare(p,(unsigned char*)"1025",4)) {
            printf("ERROR: \"1025\"\n");
            return 1;
        }
        printf("SUCCESS\n\n");
        zfree(zl);
    }

    printf("Merge test:\n");
    {
        /* create list gives us: [hello, foo, quux, 1024] */
        zl = createList();
        unsigned char *zl2 = createList();

        unsigned char *zl3 = ziplistNew();
        unsigned char *zl4 = ziplistNew();

        if (ziplistMerge(&zl4, &zl4)) {
            printf("ERROR: Allowed merging of one ziplist into itself.\n");
            return 1;
        }

        /* Merge two empty ziplists, get empty result back. */
        zl4 = ziplistMerge(&zl3, &zl4);
        ziplistRepr(zl4);
        if (ziplistLen(zl4)) {
            printf("ERROR: Merging two empty ziplists created entries.\n");
            return 1;
        }
        zfree(zl4);

        zl2 = ziplistMerge(&zl, &zl2);
        /* merge gives us: [hello, foo, quux, 1024, hello, foo, quux, 1024] */
        ziplistRepr(zl2);

        if (ziplistLen(zl2) != 8) {
            printf("ERROR: Merged length not 8, but: %u\n", ziplistLen(zl2));
            return 1;
        }

        p = ziplistIndex(zl2,0);
        if (!ziplistCompare(p,(unsigned char*)"hello",5)) {
            printf("ERROR: not \"hello\"\n");
            return 1;
        }
        if (ziplistCompare(p,(unsigned char*)"hella",5)) {
            printf("ERROR: \"hella\"\n");
            return 1;
        }

        p = ziplistIndex(zl2,3);
        if (!ziplistCompare(p,(unsigned char*)"1024",4)) {
            printf("ERROR: not \"1024\"\n");
            return 1;
        }
        if (ziplistCompare(p,(unsigned char*)"1025",4)) {
            printf("ERROR: \"1025\"\n");
            return 1;
        }

        p = ziplistIndex(zl2,4);
        if (!ziplistCompare(p,(unsigned char*)"hello",5)) {
            printf("ERROR: not \"hello\"\n");
            return 1;
        }
        if (ziplistCompare(p,(unsigned char*)"hella",5)) {
            printf("ERROR: \"hella\"\n");
            return 1;
        }

        p = ziplistIndex(zl2,7);
        if (!ziplistCompare(p,(unsigned char*)"1024",4)) {
            printf("ERROR: not \"1024\"\n");
            return 1;
        }
        if (ziplistCompare(p,(unsigned char*)"1025",4)) {
            printf("ERROR: \"1025\"\n");
            return 1;
        }
        printf("SUCCESS\n\n");
        zfree(zl);
    }

    printf("Stress with random payloads of different encoding:\n");
    {
        int i,j,len,where;
        unsigned char *p;
        char buf[1024];
        int buflen;
        list *ref;
        listNode *refnode;

        /* Hold temp vars from ziplist */
        unsigned char *sstr;
        unsigned int slen;
        long long sval;

        for (i = 0; i < 20000; i++) {
            zl = ziplistNew();
            ref = listCreate();
            listSetFreeMethod(ref,(void (*)(void*))sdsfree);
            len = rand() % 256;

            /* Create lists */
            for (j = 0; j < len; j++) {
                where = (rand() & 1) ? ZIPLIST_HEAD : ZIPLIST_TAIL;
                if (rand() % 2) {
                    buflen = randstring(buf,1,sizeof(buf)-1);
                } else {
                    switch(rand() % 3) {
                    case 0:
                        buflen = sprintf(buf,"%lld",(0LL + rand()) >> 20);
                        break;
                    case 1:
                        buflen = sprintf(buf,"%lld",(0LL + rand()));
                        break;
                    case 2:
                        buflen = sprintf(buf,"%lld",(0LL + rand()) << 20);
                        break;
                    default:
                        assert(NULL);
                    }
                }

                /* Add to ziplist */
                zl = ziplistPush(zl, (unsigned char*)buf, buflen, where);

                /* Add to reference list */
                if (where == ZIPLIST_HEAD) {
                    listAddNodeHead(ref,sdsnewlen(buf, buflen));
                } else if (where == ZIPLIST_TAIL) {
                    listAddNodeTail(ref,sdsnewlen(buf, buflen));
                } else {
                    assert(NULL);
                }
            }

            assert(listLength(ref) == ziplistLen(zl));
            for (j = 0; j < len; j++) {
                /* Naive way to get elements, but similar to the stresser
                 * executed from the Tcl test suite. */
                p = ziplistIndex(zl,j);
                refnode = listIndex(ref,j);

                assert(ziplistGet(p,&sstr,&slen,&sval));
                if (sstr == NULL) {
                    buflen = sprintf(buf,"%lld",sval);
                } else {
                    buflen = slen;
                    memcpy(buf,sstr,buflen);
                    buf[buflen] = '\0';
                }
                assert(memcmp(buf,listNodeValue(refnode),buflen) == 0);
            }
            zfree(zl);
            listRelease(ref);
        }
        printf("SUCCESS\n\n");
    }

    printf("Stress with variable ziplist size:\n");
    {
        stress(ZIPLIST_HEAD,100000,16384,256);
        stress(ZIPLIST_TAIL,100000,16384,256);
    }

    return 0;
}
#endif
