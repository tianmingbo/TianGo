//
// Created by 田明博 on 2024/5/13.
// 把字符串看成指针
//
#include "stdio.h"


int main() {
    printf("%s,%p,%c", "we", "are", *"tian"); //p是are的首字母地址,*"tian"是字符串的首字母的地址指向的值
    return 0;
}
