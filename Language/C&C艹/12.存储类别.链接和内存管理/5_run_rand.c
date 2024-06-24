//
// Created by 田明博 on 2024/5/18.
// 生成一个随机数
//
#include "stdio.h"

extern void set_rand(unsigned int send);

extern int rand();

int main() {
    puts("input seed");
    unsigned int seed;
    while (scanf("%u", &seed) == 1) {
        set_rand(seed);//重置seed
        for (int i = 0; i < 5; i++)
            printf("res is:%d\n", rand());
        printf("Please enter next seed ( q to quit ) : \n");
    }
    puts("done");
    return 0;
}