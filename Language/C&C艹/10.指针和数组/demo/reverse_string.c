/**
 * 编写函数reverse_string,它的原型如下:
 *      void reverse_string(char *string);
 * 函数把参数字符串中的字符反向排列。请使用指针而不是数组下标,不要使用任何C函数库中用于操纵字符串的函数。
 * 提示:不需要声明一个局部数组来临时存储参数字符串。
 * */

#include "stdio.h"
#include "string.h"

void reverse_string(char *string);

int main() {
    char str[] = "tian";
    reverse_string(str);
    puts(str);
    return 0;
}

void reverse_string(char *string) {
    if (string == NULL)
        return;

    size_t len = strlen(string);
//    printf("%zu\n", len - 10); //无符号数，这个输出不会<0
    if (len <= 1)
        return;

    char *left = string;
    char *right = string + len - 1;

    while (left < right) {
        char tmp = *left;
        *left++ = *right;
        *right-- = tmp;
    }
}