//使用指向结构的指针

#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define NLEN 30

struct namect {
    char fname[NLEN];
    char lname[NLEN];
    int letters;
};

void getinfo(struct namect *);

void makeinfo(struct namect *);

void showinfo(const struct namect *);

char *get_s(char *st, int n);

int main() {
    struct namect person;
    getinfo(&person);
    makeinfo(&person);
    showinfo(&person);
    return 0;
}

void getinfo(struct namect *person) {
    puts("input fname:");
    get_s(person->fname, NLEN);
    puts("input lname:");
    get_s(person->lname, NLEN);
}

void makeinfo(struct namect *person) {
    person->letters = strlen(person->fname) + strlen(person->lname);
}

void showinfo(const struct namect *person) {
    puts("user info:\n");
    printf("fname is %s, lname is %s, name length is %d\n", person->fname, person->lname, person->letters);
}

char *get_s(char *st, int n) {

    char *ret;
    ret = fgets(st, NLEN, stdin);
    if (ret) {
        char *find = strchr(st, '\n');
        if (find)
            *find = '\0';
        else
            while (getchar() != '\n')
                continue;
    }
    return ret;
}
