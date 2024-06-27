#include "stdio.h"

static size_t strlen(char *str) {
    int count = 0;
    while (*str++ != '\0') //注意\n
        count++;
    return count;
}

int main() {
    char input[1000];
    char *str = fgets(input, 1000, stdin);
    size_t res = strlen(str);
    printf("%zu", res);
    return 0;
}