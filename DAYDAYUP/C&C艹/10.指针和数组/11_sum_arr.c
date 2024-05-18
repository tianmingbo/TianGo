//
// Created by tmb on 24-4-28.
// 10.指针和数组
//
#include "stdio.h"

#define MONTHS 12

int sum(int *start, const int *end);

int main(void) {
    int days[MONTHS] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int res = sum(days, days + MONTHS);
    printf("res is: %d\n", res);
    return 0;
}

int sum(int *start, const int *end) {
    int total = 0;
    while (start < end) {
        total += *start++;
//        start++; //指针指向下一个元素
    }
    return total;
}