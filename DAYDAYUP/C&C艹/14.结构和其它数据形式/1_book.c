//
// Created by 田明博 on 2024/5/21.
//

#include "stdio.h"
#include "string.h"

#define MAXTITL 41
#define MAXAUTH  31

char *get_s(char *st, int n);

struct book {
    char title[MAXTITL];
    char author[MAXAUTH];
    float value;
};

int main() {
    struct book library;
    puts("input book title");
    get_s(library.title, MAXTITL);
    puts("input book author");
    get_s(library.author, MAXAUTH);
    puts("input book value");
    scanf("%f", &library.value);
    printf("%s by %s: $%f\n", library.title, library.author, library.value);
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