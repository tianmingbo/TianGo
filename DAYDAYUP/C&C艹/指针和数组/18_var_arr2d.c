//
// Created by 田明博 on 2024/4/28.
// 变长数组
// 声明一个带二维变长数组参数的函数，如下所示：
//    int sum2d(int rows, int cols, int ar[rows][cols]);
//

#include "stdio.h"

#define ROWS 3
#define COLS 4

int sum2d(int rows, int cols, int ar[rows][cols]);

int main() {
    int junk[ROWS][COLS] = {
            {2,  4,  6, 8},
            {1,  3,  5, 7},
            {12, 10, 8, 6}
    };
    int res = sum2d(ROWS, COLS, junk);
    printf("res is:%3d", res);
    return 0;
}

int sum2d(int rows, int cols, int ar[rows][cols]) {
    int total = 0;
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            total += ar[i][j];
    return total;
}