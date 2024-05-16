//
// Created by 田明博 on 2024/5/16.
// 字符串复制
//

#include <string.h>
#include "stdio.h"

#define SIZE 30
#define LIM 5

char *s_gets(char *st, int n);

int main() {
    char words[LIM][SIZE];
    char tmp[SIZE];
    int i = 0;
    puts("input start with q word:");
    while (i < LIM && s_gets(tmp, SIZE)) {
        if (*tmp != 'q')
            puts("need start with q");
        else {
            strcpy(words[i], tmp);
            i++;
        }
    }
    puts("this is word:");
    for (int j = 0; j < LIM; j++) {
        puts(words[j]);
    }
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