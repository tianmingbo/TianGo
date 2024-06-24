//
// Created by 田明博 on 2024/5/18.
//多文件
/**
 * 多文件编译
 * gcc -c 2_parta.c -o parta
 * gcc -c 3_partb.c -o partb
 * gcc parta partb -o test
 * */
# include <stdio.h>

void report_count();

void accumulate(int k); //除非使用 static 关键字，否则一般函数声明都默认为  extern。

int count = 0;

int main(void) {
    int value;
    register int i;//寄存器变量
    printf("Enter a positive integer (0 to quit ) : ");
    while (scanf("%d", &value) == 1 && value > 0) {
        ++count;// 使用文件作用域变量
        for (i = value; i >= 0; i--)
            accumulate(i);
        printf("Enter a positive integer (0 to quit ) : ");
    }

    report_count();
    return 0;
}

void report_count() {
    printf("Loop executed %d times \n", count);
}