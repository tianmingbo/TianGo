//把结构成员作为参数传递
#include "stdio.h"
#include "stdlib.h"

#define FUNCDLEN 50

double sum(double, double);

struct funds {

    char bank[FUNCDLEN];
    double bankfund;
    char save[FUNCDLEN];
    double savefund;

};

int main() {
    struct funds stan = {
            "ICBC",
            2222.2,
            "NH",
            8834.324
    };
    printf("stan has a total of $%.2f.\n", sum(stan.bankfund, stan.savefund));
    return 0;
}

double sum(double a, double b) {
    return (a + b);
}
