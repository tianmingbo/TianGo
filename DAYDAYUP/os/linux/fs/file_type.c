//
// Created by 田明博 on 2024/5/29.
//
//获取文件类型

#include "apue.h"


int main(int argc, char *argv[]) {
    if (argc < 2) {
        errno = ENOENT;
        perror(argv[0]);
        exit(0);
    }
    struct stat file_info;
    char *ptr;
    for (int i = 1; i < argc; i++) {
        printf("%s: ", argv[i]);
        //lstat检测符号链接
        if (lstat(argv[i], &file_info) < 0) {
            err_ret("stat err");
            continue;
        }
        if (S_ISBLK(file_info.st_mode))
            ptr = "块特殊文件";
        else if (S_ISCHR(file_info.st_mode))
            ptr = "字符特殊文件";
        else if (S_ISDIR(file_info.st_mode))
            ptr = "目录文件";
        else if (S_ISFIFO(file_info.st_mode))
            ptr = "管道";
        else if (S_ISREG(file_info.st_mode))
            ptr = "普通文件";
        else if (S_ISLNK(file_info.st_mode))
            ptr = "符号链接";
        else if (S_ISSOCK(file_info.st_mode))
            ptr = "套接字";
        else
            ptr = "unknown";
        puts(ptr);
    }
    return 0;
}