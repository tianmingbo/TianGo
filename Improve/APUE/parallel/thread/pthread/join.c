/**
 * int pthread_join(pthread_t thread, void **value_ptr)
 * thread: 要等待的线程标识符，即要等待的线程 ID。
 * retval: 线程的退出状态.如果不需要返回值，可以传 NULL。
 * */
#include "stdio.h"
#include "stdlib.h"
#include "pthread.h"

void *func1(void *arg) {
    puts("thread1 return");
    return ((void *) 1);
}

void *func2(void *arg) {
    puts("thread2 exit");
    pthread_exit((void *) 2);
}

int main() {
    int err;
    pthread_t tid1, tid2;
    void *tret;
    err = pthread_create(&tid1, NULL, func1, NULL);
    if (err) {
        puts("can not create thread1");
        exit(1);
    }
    err = pthread_create(&tid2, NULL, func2, NULL);
    if (err) {
        puts("can not create thread2");
        exit(1);
    }
    pthread_join(tid1, &tret);//等待指定的线程结束
    printf("thread1 return: %ld\n", (long) tret);
    pthread_join(tid2, &tret);
    printf("thread2 return: %ld\n", (long) tret);

    return 0;
}