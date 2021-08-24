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
    // 优化，如果小于1M，则分配2倍空间
    if (newlen < SDS_MAX_PREALLOC)
        newlen *= 2;
    else
        // 大于1M，就再额外分派1M
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
    // printf("1:%p\n", s);
    s = sdsMakeRoomFor(s, len); //s指向的是buf的地址
    if (s == NULL)
        return NULL;
    // printf("2:%p\n", s);
    sh = (void *)(s - (sizeof(struct sdshdr))); //指向结构体开始的地址
    // printf("3:%p\n", sh);

    memcpy(s + curlen, t, len); //内存复制，从s开始，偏移curlen个，再把t放到s后面
    // printf("**s:%s**", t);
    // printf("**%zu**", curlen);
    // printf("\n**%zu**\n", len);
    sh->len = curlen + len;
    sh->free = sh->free - len;
    s[curlen + len] = '\0';
    return s;
}

//释放给定的sds
void sdsfree(sds s)
{
    if (s == NULL)
        return;
    free(s - sizeof(struct sdshdr));
}

//把t追加到 sds的末尾
sds sdscat(sds s, const char *t)
{
    return sdscatlen(s, t, strlen(t));
}

sds sdscpylen(sds s, const char *t, size_t len)
{
    struct sdshdr *sh = (void *)(s - (sizeof(struct sdshdr)));
    printf("%d\n", sh->len);
    printf("%d\n", sh->free);
    size_t totlen = sh->free + sh->len;
    if (totlen < len) //如果空间不够，申请空间
    {
        s = sdsMakeRoomFor(s, len - sh->len);
        if (s == NULL)
            return NULL;
        sh = (void *)(s - (sizeof(struct sdshdr)));
        totlen = sh->free + sh->len;
    }
    // 复制
    memcpy(s, t, len);
    // 终止符号
    s[len] = '\0';
    sh->len = len;
    sh->free = totlen - len;
    printf("%d\n", sh->len);
    printf("%d\n", sh->free);
    return s;
}

sds sdscpy(sds s, const char *t)
{
    return sdscpylen(s, t, strlen(t));
}

sds sdstrim(sds s, const char *cset)
{
    // 只能取出两边的字符，内部字符不能去除
    struct sdshdr *sh = (void *)(s - sizeof(struct sdshdr));
    char *start, *end, *sp, *ep;
    size_t len;
    sp = start = s;
    end = ep = s + sdslen(s) - 1;
    // 双指针
    while (sp <= end && strchr(cset, *sp))
    {
        sp++;
        printf("%s\n", "flag");
    }
    while (ep > start && strchr(cset, *ep))
        ep--;
    // 判断是不是全删除了
    len = (sp > ep) ? 0 : ((ep - sp) + 1);
    // 如果有删除，就移动
    if (sh->buf != sp)
        memmove(sh->buf, sp, len);
    sh->buf[len] = '\0';
    // 重新给len和free赋值
    sh->len = len;
    sh->free = sh->free + (sh->len - len);
    return s;
}

void sdsrange(sds s, int start, int end)
{
    struct sdshdr *sh = (void *)(s - (sizeof(struct sdshdr)));
    size_t newlen, len = sdslen(s);
    if (len == 0)
        return;
    //对负值索引做判断
    if (start < 0)
    {
        start = len + start;
        if (start < 0)
            start = 0;
    }
    if (end < 0)
    {
        end = len + end;
        if (end < 0)
            end = 0;
    }
    newlen = (start > end) ? 0 : (end - start) + 1;
    if (newlen != 0)
    {
        if (start >= (signed)len)
        {
            newlen = 0;
        }
        else if (end > (signed)len)
        {
            end = len - 1;
            newlen = (start > end) ? 0 : (end - start) + 1;
        }
    }
    else
    {
        start = 0;
    }
    if (start && newlen)
        memmove(sh->buf, sh->buf + start, newlen);
    sh->buf[newlen] = 0;
    sh->free = sh->free + (sh->len - newlen);
    sh->len = newlen;
}

sds sdsup(const sds s)
{
    return sdsnewlen(s, sdslen(s));
}

sds sdsgrowzero(sds s, size_t len)
{
    struct sdshdr *sh = (void *)(s - (sizeof(struct sdshdr)));
    size_t totlen, curlen = sh->len;
    if (len < curlen)
        return s;
    s = sdsMakeRoomFor(s, len - curlen);
    if (s == NULL)
        return NULL;
    sh = (void *)(s - (sizeof(struct sdshdr)));
    memset(s + curlen, 0, (len - curlen + 1)); //填充0
    totlen = sh->len + sh->free;
    sh->len = len;
    sh->free = totlen - len;
    return s;
}

int main(int argc, char const *argv[])
{
    int lens;
    sds x = sdsnew("tian"), y;
    // printf("x->:%s\n", x);
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
    sdscat(x, " is a good man");
    // sdsfree(x);
    // x = sdscpy(x, "a");
    // sdstrim(x, "tn");
    // sdsrange(x, 1, 2);
    // y = sdsup(x);
    // printf("x->:%s\n", y);
    // y = sdsgrowzero(x, 100);
    printf("x->:%s\n", y);
    return 0;
}
