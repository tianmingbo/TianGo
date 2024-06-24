//
// Created by 田明博 on 2024/5/15.
// 使用fgets和fputs
//

#include "stdio.h"

#define SLEN 14

int main() {
    char words[SLEN];
    puts("Enter a string:");
    fgets(words, SLEN, stdin);//存储 tian\n\0
    puts("1");
    puts(words); //输出tian\n\0\n  puts会在末尾加\n
    fputs(words, stdout); //输出tian\n\0
    puts("2");
    fgets(words, SLEN, stdin);//输入tiantiantiantian, 存储tiantiantiant\0
    puts(words);
    fputs(words, stdout);
    return 0;
}