/**
 * 编写一个名叫my_strlen的函数。它类似于strlen函数,但它能够处理由于使用strn-
 * 函数而创建的未以NUL字节结尾的字符串。你需要向函数传递一个参数,它的值就是保存了需要进行长度测试的字符串的数组的长度。
 * */
#include "string.h"
#include "stdio.h"

size_t my_strlen(const char *strings, int size) {
    size_t len;
    for (len = 0; len < size; len++) {
        if (*strings++ == '\0')
            break;
    }
    return len;
}

int main() {
    char msg[] = "abcdefghijklmnopqrstuvwxyz";
    char dest[5];
    strncpy(dest, msg, 5);
    printf("%zu\n", strlen(dest)); //31,strncpy不保证'\0'结尾
    size_t len = my_strlen(dest, 5);
    printf("%zu\n", len);//5
    return 0;
}