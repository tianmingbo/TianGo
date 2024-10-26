//
// Created by 田明博 on 24-9-17.
//

#include <pthread.h>
#include <stdio.h>
#include "unistd.h"

void *thread_function(void *arg) {
    printf("Thread is running\n");
    sleep(2);  // 模拟一些操作
    printf("Thread finished\n");
    return NULL;
}

int main() {
    pthread_t thread;

    // 创建线程
    if (pthread_create(&thread, NULL, thread_function, NULL) != 0) {
        perror("Failed to create thread");
        return 1;
    }

    // 设置线程为分离状态
    if (pthread_detach(thread) != 0) {
        perror("Failed to detach thread");
        return 1;
    }

    // 主线程不等待子线程
    printf("Main thread finished\n");

    // 主线程完成时，子线程仍在运行
    sleep(3);  // 等待子线程完成
    return 0;
}
