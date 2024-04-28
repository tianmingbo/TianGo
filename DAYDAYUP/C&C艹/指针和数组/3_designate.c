//
// Created by 田明博 on 2024/4/27.
// 指定初始化器,初始化数组中的部分
//

#include "stdio.h"

#define MONTHS 4

int main() {
    const int arr[MONTHS] = {[2]=3};//指定初始化index 2,如果不指定数组大小,编译器会把数组大小设置为足够装得下初始化的值
    for (int i = 0; i < sizeof(arr) / sizeof(arr[0]); ++i) {
        printf("%14d", arr[i]);
    }
    return 0;
}