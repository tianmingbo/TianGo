//
// Created by 田明博 on 2024/5/16.
// 字符串比较
// strcmp如果相同,返回0, 前面大,返回正数. 后面大,返回复数
//

#include <string.h>
#include "stdio.h"

#define SIZE 30
#define ANSWER "Tian"

char *s_gets(char *st, int n);

int main() {
    char msg[SIZE];
    puts("input string:");
    s_gets(msg, SIZE);
    // strncmp可以限定只比较几个字符
    while (strcmp(msg, ANSWER) != 0 && strncmp(msg, ANSWER, 4) != 0) {
        puts("Wrong, try again");
        s_gets(msg, SIZE);
    }
    puts("Right");
    return 0;
}


char *s_gets(char *st, int n) {
    char *ret_val;
    int i = 0;
    ret_val = fgets(st, n, stdin);
    if (ret_val) {
        while (st[i] != '\n' && st[i] != '\0')
            i++;
        if (st[i] == '\n')
            st[i] = '\0';
        else
            while (getchar() != '\n')
                continue;
    }
    return ret_val;
}