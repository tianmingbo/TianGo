/**
 * 编写一个名叫my_strcpy_end的函数取代strcpy函数,它返回一个指向目标字符串末尾的指针(也就是说,指向NUL字节的指针),
 * 而不是返回一个指向目标字符串起始位置的指针。
 * */
#include "stdio.h"

char *my_strcpy_end(char *dest, const char *src) {
    while ((*dest++ = *src++) != '\0');
    return dest - 1;
}

int main() {
    char dest[5] = "abc";
    char *src = "tian";
    char *p = my_strcpy_end(dest, src);

    //输出dest
    p--;
    while (p >= dest) {
        printf("%c", *p--);
    }
    return 0;
}