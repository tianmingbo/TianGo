//
// Created by 田明博 on 2024/6/4.
// 一次读取一行

#include "stdio.h"
#include "stdlib.h"
#include "string.h"

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fputs("Usage..", stderr);
        exit(1);
    }
    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL) {
        perror("fopen()");
        exit(1);
    }

    char *line = NULL;
    size_t linecap = 0;
    ssize_t linelen;
    while ((linelen = getline(&line, &linecap, fp)) > 0) {
        puts(line);
        printf("linecap:%zu\n", linecap);
        printf("linelen:%zu\n", linelen);
        puts("**************");
    }

    exit(0);
}