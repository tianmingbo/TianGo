//
// Created by 田明博 on 2024/5/21.
// 复合字面量

#include "stdio.h"

#define MaxTitle 40
#define MaxAuth 20

struct book {
    char name[MaxTitle];
    char author[MaxAuth];
    float val;
};

int main() {
    struct book readfirst;
    int score;
    printf(" Enter test score : ");
    scanf(" %d", &score);
    if (score >= 84)
        readfirst = (struct book) {"Crime and Punishment ",
                                   "FyodorDostoyevsky ", 11.2};
    else
        readfirst = (struct book) {"Mr Bouncy's Nice Hat ",
                                   "Fred Winsome", 5.99};
    printf(" Your assigned reading : \n ");
    printf("%s by %s : $%.2f\n ", readfirst.name, readfirst.author, readfirst.val);
    return 0;
}