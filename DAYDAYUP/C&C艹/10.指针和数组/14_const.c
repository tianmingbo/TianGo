//
// Created by 田明博 on 2024/4/27.
// const使用
// const放在＊左侧任意位置， 限定指针指向的数据不能改变. const放在＊的右侧，限定了指针本身不能改变。
//

#include "stdio.h"

#define MONTHS 4

int main() {
    const int arr[5] = {12, 3, 4}; //数组不可修改

    //常量指针,指针指向的值不能修改,指针本身可以指向别的位置
    double rates[5] = {1.1, 2.2, 3, 4};
    const double *pd = rates;
    //    *pd=3; 不允许
    pd++; //可以指向别处
    printf("%f", *pd);

    //指向常量的指针：通过在指针变量名前加上const关键字，可以声明一个指向常量的指针，即指针本身不可以修改指向的值，但所指向的值可以被修改
    int value = 10;
    int *const ptr = &value;
    *ptr = 11;
    //ptr++; 不允许

    //常量指针指向常量：使用const关键字同时修饰指针类型和指针变量名，可以声明一个指向常量的常量指针，既不能修改指针的值，也不能修改所指向的值
    const int *const ptr1 = &value;
    //ptr1++;
    //*ptr1 = 10;
    return 0;
}