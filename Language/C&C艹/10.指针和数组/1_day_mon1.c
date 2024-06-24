//
// Created by 田明博 on 2024/4/27.
//

#include "stdio.h"

#define MONTHS 12

int main() {
    const int arr[MONTHS] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
    for (int i = 0; i < sizeof(arr) / sizeof(arr[0]); ++i) {
        printf("%4d", arr[i]);
    }
    return 0;
}