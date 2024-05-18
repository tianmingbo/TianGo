//
// Created by 田明博 on 2024/5/8.
// 复合字面量
//

#include "stdio.h"

#define COLS 4


int sum(const int ar[], int n);

int sum2d(const int ar[][COLS], int rows);

int main() {
    int total1, total2, total3;
    int *pt1;
    int(*pt2)[COLS];
    pt1 = (int[2]) {10, 20};//(int[2]) {10, 20}  复合字面量,一个匿名数组
    pt2 = (int[2][COLS]) {{1, 2, 3, 4},
                          {5, 6, 7, 8}};
    total1 = sum(pt1, 2);
    total2 = sum2d(pt2, 2);
    total3 = sum((int[3]) {1, 2, 3}, 3);
    printf("%d,%d,%d", total1, total2, total3);
    return 0;
}

int sum(const int ar[], int n) {
    int res = 0;
    for (int i = 0; i < n; i++)
        res += ar[i];

    return res;
}

int sum2d(const int ar[][COLS], int rows) {
    int res = 0;
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < COLS; j++)
            res += ar[i][j];
    return res;
}