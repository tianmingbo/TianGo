//
// Created by 田明博 on 2024/6/21.
// 钩子函数  int atexit(void (*function)(void));

#include "stdlib.h"
#include "stdio.h"

static void my_exit1(void);

static void my_exit2(void);

int main() {
    puts("begin");
    if (atexit(my_exit2) != 0) {
        perror("atexit()"); //按照注册顺序的倒序执行
        exit(1);
    }
    if (atexit(my_exit1) != 0) {
        perror("atexit()");
        exit(1);
    }
    if (atexit(my_exit1) != 0) {
        perror("atexit()");
        exit(1);
    }
    puts("end");
    exit(0);
}

/**
begin
end
first
first
second
 * */


static void my_exit1(void) {
    puts("first");
}

static void my_exit2(void) {
    puts("second");
}
