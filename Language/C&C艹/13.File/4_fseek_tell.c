/**
 * fseek()设置文件位置
 * int fseek(FILE *stream, long int offset, int origin);
    stream 是文件指针，指向要进行定位的文件。
    offset 是相对于 origin 的偏移量，可以为正数、负数或零。
    origin 可以取以下值：
    SEEK_SET : 文件开始位置
    SEEK_CUR : 文件当前位置
    SEEK_END : 文件末尾位置

 * ftell() 获取当前指针指向的位置
 * */

#include "stdio.h"
#include "stdlib.h"

int main() {
    FILE *fp = fopen("13.File/1_count.c", "r");
    if (fp == NULL) {
        puts("open file err");
        exit(EXIT_FAILURE);
    }
    //移动指针到文件结尾
    fseek(fp, 0, SEEK_END);
    //获取当前位置
    long pos = ftell(fp);
    printf("pos is:%ld\n", pos);
    //从当前位置前移10
    fseek(fp, -10, SEEK_CUR);
    pos = ftell(fp);
    printf("pos is:%ld\n", pos);
    return 0;
}