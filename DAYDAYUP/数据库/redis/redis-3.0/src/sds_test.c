#include <stdio.h>
#include <string.h>
#include <stdlib.h>
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
    sh = malloc(200 * sizeof(struct sdshdr) + 5); //申请空间
    strcpy(sh->buf, init);
    sh->free = 0;
    sh->len = 5;
    // printf("%s\n", sh->buf);
    // printf("%d\n", sh->free);
    // printf("%d\n", sh->len);
    // return (char *)sh->buf;
    return sh->buf;
}

sds sdsnew(const char *init)
{
    size_t initlen = (init == NULL) ? 0 : strlen(init);
    printf("%s", init);
    return sdsnewlen(init, initlen);
}

static inline size_t sdslen(const sds s)
{
    struct sdshdr *sh = (void *)(s - (sizeof(struct sdshdr)));
    return sh->len;
}

int main(int argc, char const *argv[])
{
    int lens;
    sds x = sdsnew("foo");
    printf("x->:%s\n", x);
    // char a[10] = "123";
    char *tmp = sdsnewlen("tian", 4);
    /*
    除了字符数组以外，c语言还支持另外一种表示字符的方法，就是直接使用一个指针指向字符串，例如：
    char *str = "http://c.biancheng.net";
    或者：
    char *str;
    str = "http://c.biancheng.net";
    */
    // printf("%s\n", x);
    printf("%s\n", tmp);
    lens = sdslen(tmp);
    printf("%d\n", lens);

    return 0;
}
