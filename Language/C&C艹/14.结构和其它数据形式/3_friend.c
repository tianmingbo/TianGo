//
// Created by 田明博 on 2024/5/21.
// 嵌套结构体
//

#include "stdio.h"
#include "string.h"

char *get_s(char *st, int n);

struct person {
    int age;
    char name[20];
};

struct guy {
    struct person friend;
    char job[40];
    float income;
};

int main() {
    struct guy tian = {
            {18, "tian"}, "IT", 180000000
    };
    printf("Dear %s\n\n", tian.friend.name);
    printf("My job is %s.\n", tian.job);
    printf("My income is %f\n", tian.income);
    puts("Done.");
    return 0;
}

char *get_s(char *st, int n) {
    char *ret;
    ret = fgets(st, n, stdin);
    if (ret) {
        //去掉fgets()储存在字符串中的换行符
        char *find = strchr(ret, '\n');
        if (find)
            *find = '\0';
        else
            while (getchar() != '\n')
                continue;
    }
}