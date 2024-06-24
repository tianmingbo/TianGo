//
// Created by 田明博 on 2024/6/13.
// 求文件长度
#include "stdio.h"
#include "stdlib.h"
#include <sys/stat.h>

static off_t flen(const char *name) {
    struct stat file_info;
    if (stat(name, &file_info) < 0) {
        perror("stat()");
        exit(1);
    }
    return file_info.st_size;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stdin, "Usage err\n");
    }
    off_t res = flen(argv[1]);
    printf("file len:%lld\n", res);
    exit(0);
}