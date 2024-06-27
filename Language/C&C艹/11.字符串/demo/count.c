/**
 * 编写一个程序,对标准输入进行扫描,并对单词"the"出现的次数进行计数。进行比较时应该区分大小写,所以"The"和"THE"并不计算在内。
 * 你可以认为各单词由一个或多个空格字符分隔,而且输入行在长度上不会超过100个字符。计数结果应该写到标准输出上。
 * */

#include "stdio.h"
#include "string.h"

#define SIZE 101

int counter(char *string) {
    int res = 0;
    char const whitespace[] = " \n\r\f\t\v";
    char *token = strtok(string, whitespace);
    while (token != NULL) {
        puts(token);
        if (strcmp(token, "the") == 0)
            res++;
        token = strtok(NULL, whitespace);
    }
    return res;
}

int main() {
    char str[SIZE];
    fgets(str, SIZE, stdin);
    printf("res is: %d\n", counter(str));
    return 0;
}