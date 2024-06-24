//
// Created by 田明博 on 2024/6/13.
// 文件截断


#include <unistd.h>
#include "stdio.h"
#include "stdlib.h"

int main() {
    const char *name = "./chmod";
    int res = truncate(name, 10);
    if (res < 0) {
        perror("truncate()");
        exit(1);
    }
    return 0;
}