
#include "stdlib.h"
#include "stdio.h"
#include "pthread.h"

#define LEFT 30000000
#define RIGHT 30000200
#define NTHR (RIGHT-LEFT+1)
struct arg_st {
    int n;
};

void *prime(void *arg) {
    int i, j, mark = 1;
    i = ((struct arg_st *) arg)->n;
    for (j = 2; j < i / 2; j++) {
        if (i % j == 0) {
            mark = 0;
            break;
        }
    }
    if (mark)
        printf("%d is a primer\n", i);

    pthread_exit(arg);
}

int main() {
    int i, err;
    pthread_t tid[NTHR];
    struct arg_st *p;
    void *ret;
    for (i = LEFT; i < RIGHT; i++) {
        p = malloc(sizeof(*p));
        if (p == NULL) {
            perror("malloc()");
            exit(1);
        }
        p->n = i;
        err = pthread_create(tid + (i - LEFT), NULL, prime, p);
        if (err) {
            puts("pthread_create error");
            exit(1);
        }
    }
    for (i = LEFT; i <= RIGHT; i++) {
        pthread_join(tid[i - LEFT], &ret);
        free(ret);
    }
    return 0;
}
