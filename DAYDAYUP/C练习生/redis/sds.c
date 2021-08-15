#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "sds.h"

//获取字符串长度
static inline size_t sdslen(const sds s)
{
    struct sdshdr *sh = (void *)(s - (sizeof(struct sdshdr)));
    return sh->len;
}


sds sdsnewlen(const char *init, size_t initlen)
{
    struct sdshdr *sh;
    if (init)
    {
        sh = malloc(sizeof(struct sdshdr) + initlen);
    }
    else
    {
        return NULL;
    }
    if (sh == NULL)
    {
        return NULL; //内存分配失败
    }
    sh->len = initlen;
    sh->free = 0;
    if (initlen && init)
    {
        memcpy(sh->buf, init, initlen);
    }
    sh->buf[initlen] = '\0';
    char *str;
    str = sh->buf;
    return str;
}

/*size_t是unsigned int
既然是无符号的,一般只能用在没有负数的地方了.比如我们的年龄啊,身高啊.在c标准函数中,最一般的就是strlen,返回字符数.字符数当然不可能是负的啊,所以函数原型是size_t strlen(const char*)
*/
sds sdsnew(const char *init)
{
    size_t initlen = (init == NULL) ? 0 : strlen(init);
    return sdsnewlen(init, initlen);
}

int main(int argc, char const *argv[])
{
    struct sdshdr *sh;
    // int length;
    uint8_t length;
    sds x = sdsnew("foo");
    printf("%s\n", x);
    printf("%d\n", memcmp(x, "foo\0", 4)); //memcmp，比较前几个字母是否相同，相同返回0
    length = sdslen(x);
    printf("%d", length);
    return 0;
}
