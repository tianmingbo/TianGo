//
// Created by 田明博 on 2024/5/16.
//

#include "stdio.h"
#include "string.h"

#define LINE 20
#define SIZE 80
#define STOP ""

char *s_gets(char *st, int n);

void str_sort(char *strings[], int num);

int main() {
    char input[LINE][SIZE];
    char *ptr[LINE];
    int count = 0;
    printf("input %d lines, and sort them\n", LINE);
    while (count < LINE && s_gets(input[count], SIZE) != NULL && input[count][0] != '\0') {
        ptr[count] = input[count];
        count++;
    }
    //排序的是指向字符串的指针,而不是字符串本身.所以input的顺序没有变化
    str_sort(ptr, count);
    puts("sorted strings:");
    for (int i = 0; i < count; i++)
        puts(ptr[i]);

    return 0;
}


void str_sort(char *strings[], int num) {
    char *temp;
    int top, seek;
    for (top = 0; top < num - 1; top++)
        for (seek = top + 1; seek < num; seek++)
            if (strcmp(strings[top], strings[seek]) > 0) {
                temp = strings[top];
                strings[top] = strings[seek];
                strings[seek] = temp;
            }
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