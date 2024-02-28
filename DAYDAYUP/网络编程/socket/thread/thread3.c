#include <string.h>
#include "stdio.h"
#include "pthread.h"
#include "semaphore.h"

#define THREAD_NUM 2
static int num;
static sem_t sem_one;
static sem_t sem_two;

void *read(void *arg);

void *accu(void *arg);

/**
 * 信号量
 * */
int main(int argc, char *argv[]) {
    pthread_t id_1, id_2;
    sem_init(&sem_one, 0, 0);
    sem_init(&sem_two, 0, 1);
    pthread_create(&id_1, NULL, read, NULL);
    pthread_create(&id_2, NULL, accu, NULL);
    pthread_join(id_1, NULL);
    pthread_join(id_2, NULL);
    sem_destroy(&sem_one);
    sem_destroy(&sem_two);
    return 0;
}

void *read(void *arg) {
    int i;
    for (i = 0; i < 5; i++) {
        fputs("input num: ", stdout);
        sem_wait(&sem_two); //调用sem-wait函数进入临界区的线程在调用sem_post函数前不允许其他线程进入临界区
        scanf("%d", &num);
        sem_post(&sem_one);
    }
    return NULL;
}

void *accu(void *arg) {
    int sum = 0, i;
    for (i = 0; i < 5; i++) {
        //在信号量为0的情况下调用sem_wait函数，该线程进入阻塞状态
        sem_wait(&sem_one);
        sum += num;
        sem_post(&sem_two);
    }
    printf("res is: %d \n", sum);
    return NULL;
}


