//
// Created by 田明博 on 2024/5/16.
// 得到输入的参数, argv[0]是程序本身的名称
//

#include "stdio.h"

int main(int argc, char *argv[]) {
    //"d d"内的是一个参数
    printf("param count is:%d\n", argc );
    for (int i = 0; i < argc; i++) {
        puts(argv[i]);
    }
    return 0;
}
