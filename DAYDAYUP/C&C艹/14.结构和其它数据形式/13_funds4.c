//把结构数组传递给函数
#include "stdio.h"

#define FUNCDLEN 50
#define N 2
struct funds {

    char bank[FUNCDLEN];
    double bankfund;
    char save[FUNCDLEN];
    double savefund;

};

double sum(const struct funds money[], int n);

int main() {
    struct funds stan[N] = {{
                                    "ICBC",
                                    2222.2,
                                    "NH",
                                    8834.324
                            },
                            {
                                    "ICBC",
                                    33232.2,
                                    "NH",
                                    2131.324
                            }};
    printf("stan has a total of $%.2f.\n", sum(stan, N));
    return 0;
}

double sum(const struct funds money[], int n) {
    double total = 0;
    for (int i = 0; i < n; i++) {
        total += money[i].bankfund + money[i].savefund;
    }
    return total;
}
