#include "stdio.h"
#include "stdlib.h"

#define LEN 20

struct names {
    char first[LEN];
    char last[LEN];
};

struct guy {
    struct names handle;
    char favfood[LEN];
    char job[LEN];
    float income;
};

int main() {
    struct guy fellow[2] = {
            {
                    {"tian", "ming"},
                    "nuddle",
                    "IT",
                    66666.6
            },
            {
                    {"da",   "li"},
                    "rich",
                    "TL",
                    100000.3
            }
    };
    struct guy *him;
    printf("address #1: %p, #2: %p\n", &fellow[0], &fellow[1]);
    him = &fellow[0]; //结构名并不是结构的地址,所以需要加上&
    printf("address #1: %p, #2: %p\n", him, him + 1);
    printf("him->income is $%.2f; (*him).income is $%.2f\n", him->income, (*him).income);
    him++;
    printf("him->favfood is %s, him->handle.last is %s\n", him->favfood, him->handle.last);

    return 0;
}
