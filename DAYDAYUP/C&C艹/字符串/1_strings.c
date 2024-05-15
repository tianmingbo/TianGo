//
// Created by 田明博 on 2024/5/13.
// 字符串的几种表现形式
//
#include "stdio.h"

#define MSG "i am a symbolic string"
#define MAXLEN 81

int main() {
    char words[MAXLEN] = "i am a string in an array";
    const char *pt1 = "point";
    puts("Here are some strings:");
    puts(MSG);
    puts(words); //puts只显示字符串,自动在末尾加上换行
    puts(pt1);
    words[9] = 't';
    puts(words);
    return 0;
}
