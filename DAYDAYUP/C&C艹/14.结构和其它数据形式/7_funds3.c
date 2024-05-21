//传递一个结构
#include "stdio.h"
#include "stdlib.h"

#define FUNCDLEN 50

struct funds {

    char bank[FUNCDLEN];
    double bankfund;
    char save[FUNCDLEN];
    double savefund;

};

double sum(struct funds);

int main() {
    struct funds stan = {
            "ICBC",
            2222.2,
            "NH",
            8834.324
    };
    printf("stan has a total of $%.2f.\n", sum(stan));
    return 0;
}

double sum(struct funds f) {
    return (f.bankfund + f.savefund);
}
