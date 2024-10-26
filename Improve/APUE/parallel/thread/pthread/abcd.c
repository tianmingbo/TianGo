//
// Created by 田明博 on 24-10-26.
// 按顺序输出abcd 使用互斥量
//

#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#define THR_NUM 4
static pthread_mutex_t mut[THR_NUM];

struct ARG {
    int n;
};

static int next(int n) {
    return (n + 1) == THR_NUM ? 0 : n + 1;
}

static void *print(void *arg) {
    int t_i = ((struct ARG *) arg)->n;
    int c = 'a' + t_i;
    while (1) {
        pthread_mutex_lock(mut + t_i);
        fputc(c, stdout);
        pthread_mutex_unlock(mut + next(t_i));
    }
    pthread_exit(NULL);
}

int main() {
    int err, i;
    pthread_t tid[THR_NUM];
    struct ARG *p;

    for (i = 0; i < THR_NUM; i++) {
        if ((p = malloc(sizeof(*p))) == NULL) {
            perror("malloc()");
            exit(1);
        }
        p->n = i;
        pthread_mutex_init(mut + i, NULL);
        pthread_mutex_lock(mut + i);
        err = pthread_create(tid + i, NULL, print, p);
        if (err) {
            perror("pthread_create()");
            exit(1);
        }
    }
    //释放第一个线程互斥量
    pthread_mutex_unlock(mut);
    alarm(1);
    for (i = 0; i < THR_NUM; i++) {
        pthread_join(tid[i], NULL);
    }
    return 0;
}
