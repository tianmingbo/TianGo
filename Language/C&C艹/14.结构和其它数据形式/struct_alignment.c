/**
 * 结构体对齐
 * */
#include "stdio.h"
#include "stddef.h"

struct Example {
    char a;
    double c;
    char b;
};

int main() {
    struct Example a = {'a', 23, 'v'};
    printf("%llu\n", sizeof(a)); //24
    printf("%llu\n", offsetof(struct Example, b)); //查看偏移量
    return 0;

}