//
// Created by 田明博 on 2024/5/16.
// 字符串拼接
//

#include "string.h"
#include "stdio.h"

#define SIZE 30
#define BUGSIZE 13

char *s_gets(char *st, int n);

int main() {
    char flower[SIZE];
    char addon[] = " smell good";
    char bug[BUGSIZE];
    int available;
    puts("what is your favorite flower?");
    s_gets(flower, SIZE);
    if ((strlen(addon) + strlen(flower) + 1) <= SIZE)
        strcat(flower, addon);  //strcat无法检查第一个数组是否能容纳第二个数组,所以需要限制
    puts(flower);

    puts("what is your favorite bug?");
    s_gets(bug, BUGSIZE);
    available = BUGSIZE - strlen(bug) - 1;
    strncat(bug, addon, available); //strncat第三个参数指定了最大添加的字符数
    puts(bug);
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