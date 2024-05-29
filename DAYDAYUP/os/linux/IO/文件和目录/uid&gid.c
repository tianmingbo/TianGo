//
// Created by 田明博 on 2024/5/29.
//
//设置用户ID（SUID）：当用户执行拥有SUID标志的可执行文件时，该程序会以文件所有者的权限来执行，而不是执行该程序的用户的权限。这通常用于特定任务，例如执行需要特权的操作但又不希望用户拥有这些特权的程序。
//设置组ID（SGID）：当用户执行拥有SGID标志的可执行文件时，该程序会以文件所属组的权限来执行，而不是执行该程序的用户的权限。这允许程序在特定组的上下文中运行，而不是当前用户的上下文中。

#include "apue.h"

int main() {
    char *path = "/etc/passwd";
    struct stat file_info;
    if (stat(path, &file_info) == 0) {
        printf("设置用户ID: %d\n", file_info.st_uid);
        printf("设置组ID: %d\n", file_info.st_gid);
        // 其他信息也可以在file_info中找到
    } else {
        perror("stat");
    }
}