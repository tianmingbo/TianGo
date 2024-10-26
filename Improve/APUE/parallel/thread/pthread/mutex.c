//信号量
/**
pthread_mutex_init()：初始化互斥锁。
pthread_mutex_lock()：加锁。
pthread_mutex_unlock()：解锁。
pthread_mutex_destroy()：销毁互斥锁。
*/

#include <stdlib.h>
#include <pthread.h>
#include <stdio.h>

pthread_mutex_t lock;

int share_count = 0;

void *calc(void *arg) {
    int i;
    pthread_mutex_lock(&lock);
    for (i = 0; i < 10000000; i++)
        share_count += 1;
    pthread_mutex_unlock(&lock);
    pthread_exit(NULL);
}

int main() {
    pthread_mutex_init(&lock, NULL);
    pthread_t t1, t2;
    int res = pthread_create(&t1, NULL, calc, NULL);
    if (res) {
        puts("create t1 err");
        exit(1);
    }
    res = pthread_create(&t2, NULL, calc, NULL);
    if (res) {
        puts("create t2 err");
        exit(1);
    }
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_mutex_destroy(&lock);
    printf("%d\n", share_count);
    return 0;
}
