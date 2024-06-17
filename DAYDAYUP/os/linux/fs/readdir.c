//
// Created by 田明博 on 2024/6/17.
// 目录遍历

#include "stdlib.h"
#include "stdio.h"
#include <dirent.h>

#define PATH "/etc"

int main() {
    DIR *dp = opendir(PATH);
    struct dirent *cur;
    if (dp == NULL) {
        perror("opendir()");
        exit(1);
    }
    while ((cur = readdir(dp)) != NULL)
        puts(cur->d_name);
    closedir(dp);
    return 0;
}