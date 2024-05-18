//
// Created by 田明博 on 2024/4/27.
//

#include "stdio.h"
#include "string.h"
int my_strlen(char *s) {
    int n;
    for (n = 0; *s != '\0'; s++)
        n++;
    return n;
}

int main() {
    char s[] = "dafafaf";
    char a=50;

    printf("len: %c\n", a);
    int n;
    n = my_strlen(s);
    printf("len: %d", n);
    return 0;
}