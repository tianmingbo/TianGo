//
// Created by 田明博 on 2024/5/18.
//多文件
#include "stdio.h"

extern int count; //引用
static int total = 0; //静态定义,内部链接

void accumulate(int k);

void accumulate(int k) {
    static int subtotal = 0;
    if (k <= 0) {
        printf("loop cycle:%d\n", count);
        printf("subtotal : %d; total : %d\n ", subtotal, total);
        subtotal = 0;
    } else {
        subtotal += k;
        total += k;
    }
}