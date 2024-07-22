#include "stdlib.h"
#include "stdio.h"
#include "pthread.h"
#include "string.h"
#include "unistd.h"

#define TNUM 4

static pthread_mutex_t mutex[TNUM]; // 定义互斥锁

typedef struct {
    int n;
} tr_arg;

static void *func(void *arg) {
    int n = ((tr_arg *) arg)->n;
    printf("%d\n", n);
    int c = 'a' + n;
    while (1) {
        pthread_mutex_lock(mutex + n);
        printf("%c", c);
        pthread_mutex_unlock(mutex + (n + 1) % TNUM);
    }

    pthread_exit(NULL);
}

int main() {
    pthread_t tid[TNUM];
    tr_arg *args = malloc(sizeof(tr_arg) * TNUM);
    int err, i;

    for (i = 0; i < TNUM; i++) {
        pthread_mutex_init(mutex + i, NULL);
        pthread_mutex_lock(mutex + i);
        (args + i)->n = i;
        err = pthread_create(tid + i, NULL, func, args + i);
        if (err) {
            fprintf(stderr, "pthread_create():%s\n", strerror(err));
            exit(1);
        }
    }
    alarm(5);
    pthread_mutex_unlock(mutex);
    for (i = 0; i < TNUM; i++) {
        pthread_join(tid[i], NULL);
    }
    free(args);
    return 0;
}