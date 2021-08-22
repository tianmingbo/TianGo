#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define SDS_MAX_PREALLOC (1024 * 1024)

typedef char *sds;

struct sdshdr
{
    // buf 中已占用空间的长度
    int len;
    // buf 中剩余可用空间的长度
    int free;
    // 数据空间
    char buf[];
};

sds sdsnewlen(const void *init, int len)
{
    struct sdshdr *sh;
    sh = malloc(sizeof(struct sdshdr) + len + 1); //申请空间
    memcpy(sh->buf, init, len);
    sh->free = 0;
    sh->len = len;
    // printf("%s\n", sh->buf);
    // printf("%d\n", sh->free);
    // printf("%d\n", sh->len);
    sh->buf[len] = '\0';
    return (char *)sh->buf;
    // return sh->buf;
}

sds sdsnew(const char *init)
{
    size_t initlen = (init == NULL) ? 0 : strlen(init);
    return sdsnewlen(init, initlen);
}

static inline size_t sdslen(const sds s)
{
    struct sdshdr *sh = (void *)(s - (sizeof(struct sdshdr)));
    return sh->len;
}

static inline size_t sdsavail(const sds s)
{
    struct sdshdr *sh = (void *)(s - (sizeof(struct sdshdr)));
    return sh->free;
}

sds sdsMakeRoomFor(sds s, size_t addlen)
{
    struct sdshdr *sh, *newsh;
    size_t free = sdsavail(s);
    size_t len, newlen;
    if (free >= addlen)
        return s;
    len = sdslen(s);
    sh = (void *)(s - (sizeof(struct sdshdr)));
    newlen = (len + addlen);
    if (newlen < SDS_MAX_PREALLOC)
        newlen *= 2;
    else
        newlen += SDS_MAX_PREALLOC;
    newsh = realloc(sh, sizeof(struct sdshdr) + newlen + 1);
    if (newsh == NULL)
        return NULL;
    newsh->free = newlen - len;
    return newsh->buf;
}

sds sdscatlen(sds s, const char *t, size_t len)
{
    struct sdshdr *sh;
    size_t curlen = sdslen(s);
    printf("1:%p\n", s);
    s = sdsMakeRoomFor(s, len);
    if (s == NULL)
        return NULL;
    printf("2:%p\n", s);
    sh = (void *)(s - (sizeof(struct sdshdr)));
    printf("3:%p\n", sh);

    memcpy(s + curlen, t, len);
    printf("**s:%s**", t);
    printf("**%zu**", curlen);
    printf("\n**%zu**\n", len);
    sh->len = curlen + len;
    sh->free = sh->free - len;
    s[curlen + len] = '\0';
    return s;
}

sds sdscat(sds s, const char *t)
{
    return sdscatlen(s, t, strlen(t));
}

int main(int argc, char const *argv[])
{
    int lens;
    sds x = sdsnew("foo");
    printf("x->:%s\n", x);
    // char a[10] = "123";
    // char *tmp = sdsnewlen("tian", 4);
    /*
    除了字符数组以外，c语言还支持另外一种表示字符的方法，就是直接使用一个指针指向字符串，例如：
    char *str = "http://c.biancheng.net";
    或者：
    char *str;
    str = "http://c.biancheng.net";
    */
    // printf("%s\n", x);
    // printf("%s\n", tmp);
    // lens = sdslen(tmp);
    // printf("%d\n", lens);
    sdscat(x, "is a good man");
    printf("x->:%s\n", x);
    return 0;
}
