//使用指针和malloc()

#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define NLEN 30

struct namect {
    char *fname;
    char *lname;
    int letters;
};

void getinfo(struct namect *);

void makeinfo(struct namect *);

void showinfo(const struct namect *);

void clean(const struct namect *);

char *get_s(char *st, int n);

int main() {
    struct namect person;
    getinfo(&person);
    makeinfo(&person);
    showinfo(&person);
    clean(&person);
    return 0;
}

void clean(const struct namect *person) {
    free(person->fname);
    free(person->lname);
}

void getinfo(struct namect *person) {
    char temp[NLEN];
    puts("input fname:");
    get_s(temp, NLEN);
    //分配内存
    person->fname = (char *) malloc(strlen(temp) + 1);
    strcpy(person->fname, temp);
    puts("input lname:");
    get_s(temp, NLEN);
    person->lname = (char *) malloc(strlen(temp) + 1);
    strcpy(person->lname, temp);
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
