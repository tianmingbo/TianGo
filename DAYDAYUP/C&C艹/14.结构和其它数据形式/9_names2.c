//传递并返回结构

#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define NLEN 30

struct namect {
    char fname[NLEN];
    char lname[NLEN];
    int letters;
};

struct namect getinfo();

struct namect makeinfo(struct namect);

void showinfo(struct namect);

char *get_s(char *st, int n);

int main() {
    struct namect person = getinfo();
    person = makeinfo(person);
    showinfo(person);
    return 0;
}

struct namect getinfo() {
    struct namect temp;
    puts("input fname:");
    get_s(temp.fname, NLEN);
    puts("input lname:");
    get_s(temp.lname, NLEN);
    return temp;
}

struct namect makeinfo(struct namect person) {
    person.letters = strlen(person.lname) + strlen(person.fname);
    return person;
}

void showinfo(struct namect person) {
    puts("user info:\n");
    printf("fname is %s, lname is %s, name length is %d\n", person.fname, person.lname, person.letters);
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
