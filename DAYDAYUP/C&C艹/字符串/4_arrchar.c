//
// Created by 田明博 on 2024/5/13.
// 指向字符串的指针数组和char类型数组的数组
//
#include "stdio.h"

#define SLEN 40
#define LIM 5

int main() {
    const char *arrstr[LIM] = {
            "dkakdk",
            "dafadf",
            "afdfaf",
            "qrytuh",
            "tyu"
    };
    char arrstr1[LIM][SLEN]={
            "rqrirj",
            "dafiuer",
            "rhierhquir",
            "123",
            "tian"
    };
    puts("compare");
    printf("arrstr size: %zd, arrstr1 size: %zd", sizeof(arrstr), sizeof(arrstr1));
    return 0;
}
