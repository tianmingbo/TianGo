//
// Created by 田明博 on 2024/5/15.
// 缩短字符串长度
//

#include "stdio.h"
#include <string.h>

void fit(char *, unsigned int);

int main() {
    //msg 被声明为 char * 类型，意味着是一个指向常量字符串的指针，而常量字符串是不可修改的。
    //msg 声明为 char msg[] 时，它实际上是一个字符数组,可以修改字符串中的内容
    char msg[] = "jafjsdjajoiroiqriojamijfjamcoaimc,fajodjsa ";
    puts(msg);
    fit(msg, 20);
    puts(msg);
    puts("输出后续:");
    puts(msg + 21);
    return 0;
}

void fit(char *msg, unsigned int size) {
    if (strlen(msg) > size)
        msg[size] = '\0';
}