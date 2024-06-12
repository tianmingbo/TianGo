//
// Created by 田明博 on 2024/6/12.
// 设置用户id和设置组id,若设置了用户id,则使用者拥有用文件所有者的权限
#include <sys/stat.h>
#include "stdio.h"
#include "stdlib.h"

int main() {
    struct stat file_info;
    if (stat("/etc/passwd", &file_info) < 0) {
        perror("stat()");
        exit(1);
    }
    if (file_info.st_mode & S_ISUID)
        printf("has Set-UID bit set");
    if (file_info.st_mode & S_ISGID)
        printf("has Set-GID bit set");
    return 0;
}