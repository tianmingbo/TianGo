//
// Created by 田明博 on 2024/6/14.
// 文件权限屏蔽字. 0666 - umask


#include <sys/stat.h>
#include <fcntl.h>
#include "stdio.h"
#include "stdlib.h"

#define RWRWRW (S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH|S_IWOTH)

int main() {
    umask(0); //不设置屏蔽位
    if (creat("foo", RWRWRW) < 0) {
        perror("create()");
        exit(1);
    }
    umask(S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
    printf("%d\n", S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
    //系统提供的默认权限（例如文件通常是 0666，目录是 0777)
    //如果文件的默认权限是 0666，而 umask 是 022，那么实际权限就会是 0644（0666 - 022)
    if (creat("bar", RWRWRW) < 0) {
        perror("create()");
        exit(1);
    }
}