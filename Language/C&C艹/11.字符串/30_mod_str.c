//
// Created by 田明博 on 2024/5/16.
// 修改字符串
//

#include "stdio.h"
#include "string.h"
#include "ctype.h"

#define SIZE 80

int get_punct_count(const char *str);

void toUpper(char *str);

int main() {
    puts("input msg:");
    char msg[SIZE];
    fgets(msg, SIZE, stdin);
    char *find = strchr(msg, '\n');
    if (find)
        *find = '\0';
    toUpper(msg);
    puts(msg);
    printf("punct count is %d:\n", get_punct_count(msg));

    return 0;
}

void toUpper(char *str) {
    //转换为大写
    while (*str) {
        *str = toupper(*str);
        str++;
    }
}

int get_punct_count(const char *str) {
    //统计标点符号个数
    int count = 0;
    while (*str) {
        if (ispunct(*str))
            count++;
        str++;

    }
    return count;
}