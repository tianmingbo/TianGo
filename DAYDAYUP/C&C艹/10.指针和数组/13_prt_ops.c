//
// Created by tmb on 24-4-28.
// 指针基本操作
//
#include "stdio.h"


int main(void) {
    int arr[5] = {1, 2, 3, 4, 5};
    int *p1, *p2, *p3;
    p1 = arr;
    p2 = &arr[2];
    //解引用指针，以及获取指针的地址
    printf("p = %p, *p = %d, &p = %p\n", p1, *p1, &p1);
    p3 = p1 + 4;
    //指针加法
    printf("p1 + 4 = %p, *(p1 + 4) = %d\n", p3, *(p1 + 4));
    //递增指针
    p1++;
    printf("p = %p, *p = %d, &p = %p\n", p1, *p1, &p1);
    //一个指针减去另一个指针
    printf("p2 = %p, p1 = %p, p2 - p1 = %ld\n", p2, p1, p2 - p1);//p2 = 0x7ffc48d39c68, p1 = 0x7ffc48d39c64, p2 - p1 = 1
    //一个指针减去一个整数
    printf("p3 = %p, *(p3 - 4) = %d\n", p2, *(p3 - 4));//p3 = 0x7ffc48d39c68, *(p3 - 4) = 1
    return 0;
}
