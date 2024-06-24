#include <string.h>
#include "stdio.h"
#include "pthread.h"


#define THREAD_NUM 2
long long num;
pthread_mutex_t mutex;

void *des(void *arg);

void *add(void *arg);

/**
 * 临界区问题
 * gcc  thread2.c  -D_REENTRANT -o mutux  -lpthread
 * -lpthread: 指定链接 pthread 库，用于支持多线程编程
 * -D_REENTRANT: 是一个预处理器宏定义参数，通常用于启用线程安全的库函数。在这种情况下，_REENTRANT 宏定义用于告知编译器需要编译支持多线程操作的代码。
 * */
int main(int argc, char *argv[]) {
    pthread_t thread_id[THREAD_NUM];
    int i;
    for (i = 0; i < THREAD_NUM; i++) {
        if (i % 2)
            pthread_create(&(thread_id[i]), NULL, add, NULL);
        else
            pthread_create(&(thread_id[i]), NULL, des, NULL);
    }
    for (i = 0; i < THREAD_NUM; i++)
        pthread_join(thread_id[i], NULL);
    printf("num is: %lld\n", num);
    return 0;
}

void *des(void *arg) {
    int i;
    for (i = 0; i < 50000; i++) {
        pthread_mutex_lock(&mutex);
        num -= 1;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

void *add(void *arg) {
    int i;
    for (i = 0; i < 50000; i++) {
        pthread_mutex_lock(&mutex); //加锁
        num += 1;
        pthread_mutex_unlock(&mutex); //释放
    }
    return NULL;
}

