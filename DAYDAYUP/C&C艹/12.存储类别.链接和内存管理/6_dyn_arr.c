//
// Created by 田明博 on 2024/5/18.
// 动态分配数组
//

#include "stdio.h"
#include "stdlib.h"

int main() {
    int number;
    puts("What i s the maximum number of type double entries? ");
    if (scanf("%d", &number) != 1) {
        puts("Number not correctly entered -- bye.");
        exit(EXIT_FAILURE);
    }
    //动态申请内存
    //    double *ptr = (double *) malloc(number * sizeof(double));
    /*
     * calloc 也用于分配内存，但与 malloc 不同的是，它会将分配的内存块中的每个字节都初始化为0。
     * calloc 接受两个参数：要分配的元素个数和每个元素的大小（以字节为单位）。
     * */
    double *ptr = (double *) calloc(number, sizeof(double));
    if (ptr == NULL) {
        //分配内存失败,退出
        puts("Memory allocation failed. Goodbye . ");
        exit(EXIT_FAILURE);
    }
    puts("Enter the values (q to quit ):");
    int i = 0;
    while (i < number && scanf("%1lf", &ptr[i]) == 1)
        ++i;
    printf("Here are your %d entries : \n ", number = i);
    for (i = 0; i < number; i++) {
        printf("%-7.2f", ptr[i]);
        if (i % 7 == 6)
            putchar('\n');
    }
    if (i % 7 != 0)
        putchar('\n');
    puts("Done.");
    free(ptr); //释放内存
    return 0;
}