//
// Created by 田明博 on 2024/4/27.
//

#include "stdio.h"

#define MONTHS 4

int main() {
    const int arr[MONTHS];
    for (int i = 0; i < sizeof(arr) / sizeof(arr[0]); ++i) {
        printf("%14d", arr[i]); //未赋值,乱码
    }
    return 0;
}