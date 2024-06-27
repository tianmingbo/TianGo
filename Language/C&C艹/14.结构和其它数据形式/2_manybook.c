//
// Created by 田明博 on 2024/5/21.
// 结构体数组
//

#include "stdio.h"
#include "string.h"

#define MAXTITL 41
#define MAXAUTH  31
#define BOOKS 2

char *get_s(char *st, int n);

typedef struct {
    char title[MAXTITL];
    char author[MAXAUTH];
    float value;
} Book;

int main() {
    Book library[BOOKS];
    int count = 0;
    while (count < BOOKS && get_s(library[count].title, MAXTITL) != NULL &&
           library[count].title[0] != '\0') {
        puts("input book author");
        get_s(library[count].author, MAXAUTH);
        puts("input book value");
        scanf("%f", &library[count].value);
        while (getchar() != '\n')
            continue;
        count++;
        printf("count:%d\n", count);
    }
    if (count) {
        puts("book list:");
        for (int i = 0; i < count; i++) {
            printf("%s by %s: $%f\n", library[i].title, library[i].author, library[i].value);
        }
    }
    puts("Done.");
    return 0;
}

char *get_s(char *st, int n) {
    char *ret;
    ret = fgets(st, n, stdin);
    if (ret) {
        //去掉fgets()储存在字符串中的换行符
        char *find = strchr(ret, '\n');
        if (find)
            *find = '\0';
        else
            while (getchar() != '\n')
                continue;
    }
}