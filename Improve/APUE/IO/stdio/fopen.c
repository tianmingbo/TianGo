//
// Created by 田明博 on 2024/6/2.
//
#include "stdio.h"
#include "stdlib.h"
#include "errno.h"
#include "string.h"

int main() {
    FILE *fp = fopen("./fwide.c ", "r");
    if (fp == NULL) {
//        fprintf(stderr, "fopen() failed! error=%d\n", errno);
        perror("fopen() failed!"); //结合errno
        fputs(strerror(errno), stderr);
        exit(1);
    }
    fputs("done", stderr);
    fclose(fp);
    exit(0);
}