//
// Created by 田明博 on 2024/7/16.
// int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine)(void *), void *arg);
//
#include "pthread.h"
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"

void *func(void *arg) {
    puts("thread is working");
    pthread_exit(NULL);
//    return NULL;
}

int main() {
    pthread_t tid;
    void *rt_ptr;
    puts("start");
    int err = pthread_create(&tid, NULL, func, NULL);
    if (err) {
        puts("pthread_create error");
        exit(1);
    }
    pthread_join(tid, &rt_ptr);
    puts("end");
    return 0;
}