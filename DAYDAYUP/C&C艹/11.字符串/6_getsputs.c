//
// Created by 田明博 on 2024/5/15.
// 使用gets和puts
//

#include "stdio.h"

#define SLEN 81

int main() {
    char words[SLEN];
    puts("Enter a string");
    gets(words); //gets不安全,不知道输入的字符串有多长,会导致缓冲区溢出
    puts(words);//输出字符串,末尾加\n
    printf("%s\n", words);
    return 0;
}