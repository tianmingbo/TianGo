/**
 * pthread_cleanup_push(void (*rtn)(void *), void *arg)
 * pthread_cleanup_pop(int execute)
 * */
#include "stdio.h"
#include "stdlib.h"
#include "pthread.h"

void cleanup(void *arg) {
    printf("cleanup: %s\n", (char *) arg);
}

void *func1(void *arg) {
    puts("thread1 return");
    pthread_cleanup_push(cleanup, "thread1 first");
        pthread_cleanup_push(cleanup, "thread1 second");
            puts("thread 1 put complete");
            if (arg)
                //如果线程是从它的启动例程中返回而终止的话,清理程序不会被调用
                return ((void *) 1);
        pthread_cleanup_pop(0);
    pthread_cleanup_pop(0);
    return ((void *) 1);

}

void *func2(void *arg) {
    puts("thread2 exit");
    pthread_cleanup_push(cleanup, "thread2 first");
        pthread_cleanup_push(cleanup, "thread2 second");
            puts("thread 2 put complete");
            if (arg)
                pthread_exit((void *) 2);
        pthread_cleanup_pop(0);
    pthread_cleanup_pop(0);
    pthread_exit((void *) 2);
}

int main() {
    int err;
    pthread_t tid1, tid2;
    void *tret;
    err = pthread_create(&tid1, NULL, func1, (void *) 1);
    if (err) {
        puts("can not create thread1");
        exit(1);
    }
    err = pthread_create(&tid2, NULL, func2, (void *) 1);
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