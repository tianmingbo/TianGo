//
// Created by 田明博 on 2024/5/22.
//
#include <stdio.h>
#include "string.h"

// 定义联合
union Data {
    int i;
    float f;
    char str[20];
};

// 定义带有数据类型标识的联合
struct Variant {
    union Data data;
    union Data *data1;
    char type;
};

int main() {
    struct Variant var;
    union Data d1;
    var.data1 = &d1;
    var.data1->i = 99;
    printf("var.data1->i: %d\n", var.data1->i);
    var.type = 'I';
    var.data.i = 42;
    printf("Data type: INT, Value: %d\n", var.data.i);

    var.type = 'F';
    var.data.f = 3.14;
    printf("Data type: FLOAT, Value: %f\n", var.data.f);

    var.type = 'S';
    strcpy(var.data.str, "Hello, Union!");
    printf("Data type: STRING, Value: %s\n", var.data.str);

    return 0;
}