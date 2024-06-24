//传递指向结构的指针
#include "stdio.h"
#include "stdlib.h"

#define FUNCDLEN 50

struct funds {

    char bank[FUNCDLEN];
    double bankfund;
    char save[FUNCDLEN];
    double savefund;

};

double sum(const struct funds *);

int main() {
    struct funds stan = {
            "ICBC",
            2222.2,
            "NH",
            8834.324
    };
    struct funds *p = &stan;
    printf("stan has a total of $%.2f.\n", sum(p));
    return 0;
}

double sum(const struct funds *money) {
    return (money->bankfund + money->savefund);
}
