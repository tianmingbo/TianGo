/**
 * 字符串复制
 * */
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

static char *str_dup(const char *string) {
    char *new_str;
    new_str = malloc(strlen(string) + 1);
    if (new_str != NULL)
        strcpy(new_str, string);
    return new_str;
}

int main() {
    char *src = "tian";
    puts(str_dup(src));
    return 0;
}