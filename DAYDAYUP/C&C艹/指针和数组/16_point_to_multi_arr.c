//
// Created by 田明博 on 2024/4/28.
// 指向多维数组的指针
//

#include "stdio.h"


int main() {
    int zip[4][2] = {{1, 2},
                     {3, 4},
                     {5, 6},
                     {7, 8}};
    int (*p)[2] = zip; //声明一个指向包含2个int元素的指针
    printf("p = %p, p + 1 = %p\n", p, p + 1);
    printf("p[0] = %p, p[0] + 1 = %p\n", p[0], p[0] + 1);
    printf("*p = %p, *p + 1 = %p\n", *p, *p + 1);
    printf("p[0][0] = %d\n", p[0][0]); //p[0][0] = 1
    printf("*p[0] = %d\n", *p[0]); //*p[0] = 1
    printf("**p = %d\n", **p); //**p = 1
    printf("p[2][1] = %d\n", p[2][1]); //p[2][1] = 6
    printf("*(*(p + 2) + 1) = %d\n", *(*(p + 2) + 1)); //*(*(p+2) + 1) = 6

    return 0;
}