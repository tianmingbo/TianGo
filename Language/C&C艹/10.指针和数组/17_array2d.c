//
// Created by 田明博 on 2024/4/28.
// 处理二维数组
//

#include "stdio.h"

#define ROWS 3
#define COLS 4

void sum_raws(int arr[][COLS]);

void sum_cols(int (*p)[COLS]);

int sum2s(int [][COLS]);

int main() {
    int junk[ROWS][COLS] = {
            {2,  4,  6, 8},
            {1,  3,  5, 7},
            {12, 10, 8, 6}
    };
    sum_raws(junk);
    sum_cols(junk);
    int res = sum2s(junk);
    printf("sum is: %d\n", res);
    return 0;
}

void sum_raws(int arr[][COLS]) {
    int total;
    for (int i = 0; i < COLS; i++) {
        total = 0;
        for (int j = 0; j < ROWS; j++)
            total += arr[j][i];
        printf("col: %d, sum = %d\n", i, total);
    }
}

void sum_cols(int (*p)[COLS]) {
    int total;
    for (int i = 0; i < ROWS; i++) {
        total = 0;
        for (int j = 0; j < COLS; j++)
            total += *(*(p + i) + j);
        printf("raw: %d, sum = %d\n", i, total);
    }
}

int sum2s(int arr[][COLS]) {
    int total = 0;
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            total += arr[i][j];
        }
    }
    return total;
}