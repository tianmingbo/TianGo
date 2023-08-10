#ifndef __REDIS_RIO_H
#define __REDIS_RIO_H

#include <stdio.h>
#include <stdint.h>
#include "sds.h"

struct _rio {
    /*
     * 定义一个函数指针，
     * read 是一个指向具有这样原型的函数的指针
     * 第一个参数是 _rio 结构体指针,表示 I/O 对象。
     * 第二个参数是 void* 指针,指向读入数据的缓冲区。
     * 第三个参数是 len,表示要读取的最大长度。
     * */
    size_t (*read)(struct _rio *, void *buf, size_t len);

    size_t (*write)(struct _rio *, const void *buf, size_t len);

    off_t (*tell)(struct _rio *);

    int (*flush)(struct _rio *);

    /* 如果不为 NULL，则 update_cksum 方法用于计算迄今为止读取或写入的所有数据的校验和。
     * 该方法应设计为可以使用当前校验和以及指向新数据块的 buf 和 len 字段来调用，以添加到校验和计算中。 */
    void (*update_cksum)(struct _rio *, const void *buf, size_t len);

    /* The current checksum */
    uint64_t cksum;

    /* number of bytes read or written */
    size_t processed_bytes;

    /* maximum single read or write chunk size */
    size_t max_processing_chunk;

    /* Backend-specific vars. */
    union {
        /* In-memory buffer target. */
        struct {
            sds ptr;
            off_t pos;
        } buffer;
        /* Stdio file pointer target. */
        struct {
            FILE *fp;
            off_t buffered; /* Bytes written since last fsync. */
            off_t autosync; /* fsync after 'autosync' bytes written. */
        } file;
        /* Multiple FDs target (used to write to N sockets). */
        struct {
            int *fds;       /* File descriptors. */
            int *state;     /* Error state of each fd. 0 (if ok) or errno. */
            int numfds;
            off_t pos;
            sds buf;
        } fdset;
    } io;
};

typedef struct _rio rio;

/* The following functions are our interface with the stream. They'll call the
 * actual implementation of read / write / tell, and will update the checksum
 * if needed. */
static inline size_t rioWrite(rio *r, const void *buf, size_t len) {
    // 通过循环一次写入指定长度的数据
    while (len) {
        // 计算本次要写入的字节数，如果有最大处理块大小限制且小于剩余长度，则使用最大处理块大小，否则使用剩余长度
        size_t bytes_to_write = (r->max_processing_chunk && r->max_processing_chunk < len) ? r->max_processing_chunk
                                                                                           : len;
        // 如果设置了更新校验和函数，则更新校验和
        if (r->update_cksum) r->update_cksum(r, buf, bytes_to_write);
        // 调用写入函数将数据写入到特定的输出流中，并检查是否写入成功（返回值为0表示失败）
        if (r->write(r, buf, bytes_to_write) == 0)
            return 0;
        // 更新缓冲区指针和剩余长度
        buf = (char *) buf + bytes_to_write;
        len -= bytes_to_write;
        // 更新已处理的字节数
        r->processed_bytes += bytes_to_write;
    }
    // 所有数据写入完成，返回1表示成功
    return 1;
}


static inline size_t rioRead(rio *r, void *buf, size_t len) {
    while (len) {
        size_t bytes_to_read = (r->max_processing_chunk && r->max_processing_chunk < len) ? r->max_processing_chunk
                                                                                          : len;
        if (r->read(r, buf, bytes_to_read) == 0)
            return 0;
        if (r->update_cksum) r->update_cksum(r, buf, bytes_to_read);
        buf = (char *) buf + bytes_to_read;
        len -= bytes_to_read;
        r->processed_bytes += bytes_to_read;
    }
    return 1;
}

static inline off_t rioTell(rio *r) {
    return r->tell(r);
}

static inline int rioFlush(rio *r) {
    return r->flush(r);
}

void rioInitWithFile(rio *r, FILE *fp);

void rioInitWithBuffer(rio *r, sds s);

void rioInitWithFdset(rio *r, int *fds, int numfds);

void rioFreeFdset(rio *r);

size_t rioWriteBulkCount(rio *r, char prefix, long count);

size_t rioWriteBulkString(rio *r, const char *buf, size_t len);

size_t rioWriteBulkLongLong(rio *r, long long l);

size_t rioWriteBulkDouble(rio *r, double d);

struct redisObject;

int rioWriteBulkObject(rio *r, struct redisObject *obj);

void rioGenericUpdateChecksum(rio *r, const void *buf, size_t len);

void rioSetAutoSync(rio *r, off_t bytes);

#endif
