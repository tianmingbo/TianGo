//
// Created by tmb on 24-4-28.
// 指针有类型
//
#include <stdio.h>

#define SIZE 4

int main(void) {
    short data[SIZE];
    short *p = data;//data就是指向了data数组第一个元素的指针
    double data2[SIZE];
    double *q = &data2[0];//结果一样
    printf("%15s %15s\n", "short", "double");
    for (int i = 0; i < SIZE; i++, p++, q++) {
        printf("point%d  %10p %10p\n", i, p, q);
    }
    /*
     * 既要知道地址，也要知道指针类型。指针+1是下一个元素的指针，而不是下一个字节的指针
     *           short          double
        point0  0x7ffc68bbe780 0x7ffc68bbe790
        point1  0x7ffc68bbe782 0x7ffc68bbe798
        point2  0x7ffc68bbe784 0x7ffc68bbe7a0
        point3  0x7ffc68bbe786 0x7ffc68bbe7a8
     * */
    return 0;
}
