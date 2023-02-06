#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <stdarg.h>
#include "zmalloc.h"
struct sdshdr
{
    int len;
    int free;
    char buf[];
};
typedef char *sds;

sds sdsnewlen(const void *init, size_t initlen)
{

    struct sdshdr *sh;

    // 根据是否有初始化内容，选择适当的内存分配方式
    // T = O(N)
    if (init)
    {
        // zmalloc 不初始化所分配的内存
        sh = zmalloc(sizeof(struct sdshdr) + initlen + 1);
    }
    else
    {
        // zcalloc 将分配的内存全部初始化为 0
        sh = zcalloc(sizeof(struct sdshdr) + initlen + 1);
    }

    // 内存分配失败，返回
    if (sh == NULL)
        return NULL;

    // 设置初始化长度
    sh->len = initlen;
    // 新 sds 不预留任何空间
    sh->free = 0;
    // 如果有指定初始化内容，将它们复制到 sdshdr 的 buf 中
    // T = O(N)
    if (initlen && init)
        memcpy(sh->buf, init, initlen);
    // 以 \0 结尾
    sh->buf[initlen] = '\0';

    // 返回 buf 部分，而不是整个 sdshdr
    return (char *)sh->buf;
}
static inline size_t sdslen(const sds s)
{
    struct sdshdr *sh = (void *)(s - (sizeof(struct sdshdr)));
    return sh->len;
}
sds sdsnew(const char *init)
{
    size_t initlen = (init == NULL) ? 0 : strlen(init);
    return sdsnewlen(init, initlen);
}
int main(int argc, char const *argv[])
{
    struct sdshdr *sh;
    sds x = sdsnew("foo"), y;
    printf("%s", x);
    return 0;
}
