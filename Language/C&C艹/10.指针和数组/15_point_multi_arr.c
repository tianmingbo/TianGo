//
// Created by 田明博 on 2024/4/28.
// 指针和多维数组的关系
//

#include "stdio.h"


int main() {
    /*
     * zip指向二维数组的第一个元素,+1即指向第二个元素,每次+8(2个int)
     * zip[0]指向二维数组的第一个元素的首元素->1, +1指向2,每次 + 4
     * */
    int zip[4][2] = {{1, 2},
                     {3, 4},
                     {5, 6},
                     {7, 8}};
    printf("zip = %p, zip + 1 = %p\n", zip, zip + 1); //zip = 0x7ff7bc226720, zip + 1 = 0x7ff7bc226728
    printf("zip[0] = %p, zip[0] + 1 = %p\n", zip[0], zip[0] + 1); //zip[0] = 0x7ff7bc226720, zip[0] + 1 = 0x7ff7bc226724
    printf("*zip = %p, *zip + 1 = %p\n", *zip, *zip + 1); //*zip = 0x7ff7bc226720, *zip + 1 = 0x7ff7bc226724
    printf("zip[0][0] = %d\n", zip[0][0]); //zip[0][0] = 1
    printf("*zip[0] = %d\n", *zip[0]); //*zip[0] = 1
    printf("**zip = %d\n", **zip); //**zip = 1
    printf("zip[2][1] = %d\n", zip[2][1]); //zip[2][1] = 6
    printf("*(*(zip+2) + 1) = %d\n", *(*(zip + 2) + 1)); //*(*(zip+2) + 1) = 6

    return 0;
}