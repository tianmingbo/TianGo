//
// Created by 田明博 on 2024/6/12.
//
#include <sys/types.h>
#include <sys/stat.h>
#include "stdio.h"
#include "stdlib.h"

int main(int argc, char *argv[]) {
    struct stat file_info;
    if (stat(argv[1], &file_info) < 0) {
        perror("stat()");
        exit(1);
    }
    //关闭group x and set group id on execution
    if (chmod(argv[1], (file_info.st_mode & ~S_IXGRP) | S_ISGID) < 0) {
        perror("chmod()");
    }
    //chmod 777
    if (chmod("./readme.md", S_IRWXU | S_IRWXG | S_IRWXO) < 0) {
        perror("chmod()");
    }
    exit(0);
}