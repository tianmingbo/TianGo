/**
 * 内存动态分配
 * void *malloc(size_t size);//分配指定大小的内存块，并返回一个指向该内存块起始地址的指针
 * void *calloc(size_t num, size_t size); //用于分配指定数量和大小的内存块，并将内存块的每个字节初始化为零，返回void* 类型的指针，指向分配的内存块的起始地址。如果分配失败，返回 NULL
 * void *realloc(void *ptr, size_t size);//重新分配已分配的内存块的大小
 * void free(void *ptr);
 * */
#include "stdio.h"
#include "stdlib.h"

int main() {
    int number;
    puts("number count:");
    if (scanf("%d", &number) != 1) {
        puts("Number not correctly entered -- bye.");
        exit(1);
    }
    //double *ptr = (double *) malloc(number * sizeof(double));
    double *ptr = (double *) calloc(number, sizeof(double));
    if (ptr == NULL) {
        puts("calloc() failed");
        exit(1);
    }
    puts("Enter the values (q to quit ):");
    int i = 0;
    while (i < number && scanf("%lf", &ptr[i]) == 1)
        ++i;
    printf("Here are your %d entries : \n", number = i);
    for (i = 0; i < number; i++)
        printf("%-7.2f", ptr[i]);

    putchar('\n');
    puts("Done.");
    free(ptr); //释放内存
    return 0;
}