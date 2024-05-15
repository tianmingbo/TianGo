//
// Created by 田明博 on 2024/5/13.
// 初始化数组把静态存储区的字符串拷贝到数组中,而初始化指针只是把字符串的地址拷贝给指针
//
#include "stdio.h"

#define MSG "a string"

int main() {
    char ar[] = MSG;
    const char *pt = MSG;
    printf("address of \"a string\": %p\n", "a string"); //address of "a string": 0x1041e8f6c
    printf("address ar: %p\n", ar); //address ar: 0x7ff7bbd1a74f
    printf("address pt: %p\n", pt); //address pt: 0x1041e8f6c
    printf("address of \"a string\": %p\n", "a string"); //address of "a string": 0x1041e8f6c

    return 0;
}
