//
// Created by 田明博 on 2024/6/23.
// 函数见跳转

#include "stdio.h"
#include <setjmp.h>

jmp_buf jmpbuffer;

void d(void) {
    printf("%s(): Begin\n", __FUNCTION__);
    printf("%s(): End\n", __FUNCTION__);
    longjmp(jmpbuffer, 1);
}

void c(void) {
    printf("%s(): Begin\n", __FUNCTION__);
    printf("%s(): call d()\n", __FUNCTION__);
    d();
    printf("%s(): d() returned\n", __FUNCTION__);
    printf("%s(): End\n", __FUNCTION__);
}

void b(void) {
    printf("%s(): Begin\n", __FUNCTION__);
    printf("%s(): call c()\n", __FUNCTION__);
    c();
    printf("%s(): c() returned\n", __FUNCTION__);
    printf("%s(): End\n", __FUNCTION__);
}

void a(void) {
    printf("%s(): Begin\n", __FUNCTION__);
    printf("%s(): call b()\n", __FUNCTION__);
    b();
    printf("%s(): b() returned\n", __FUNCTION__);
    printf("%s(): End\n", __FUNCTION__);
}

int main() {
    printf("%s(): Begin\n", __FUNCTION__);
    printf("%s(): call a()\n", __FUNCTION__);
    a();
    printf("%s(): a() returned\n", __FUNCTION__);
    printf("%s(): End\n", __FUNCTION__);
    //setjmp: 若直接调用,则返回0,若从longjmp返回,则为非0
    if (setjmp(jmpbuffer) != 0)
        puts("done");
    return 0;
}