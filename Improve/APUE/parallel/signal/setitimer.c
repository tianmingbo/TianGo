//
// Created by 田明博 on 2024/7/10.
//
/**
 * int setitimer(int which, const struct itimerval *new_value, struct itimerval *old_value);
 * which：指定要设置的定时器类型。可以是 ITIMER_REAL（真实时间定时器）、ITIMER_VIRTUAL（虚拟时间定时器）或者 ITIMER_PROF（CPU时间定时器）。
 *      ITIMER_REAL：产生 SIGALRM 信号，用于实现真实时间的定时。
 *      ITIMER_VIRTUAL：产生 SIGVTALRM 信号，用于实现进程在用户态运行的虚拟时间的定时。
 *      ITIMER_PROF：产生 SIGPROF 信号，用于实现进程在用户态和内核态的总运行时间的定时。
 * new_value：指向 struct itimerval 结构体的指针，描述了新的定时器设置。struct itimerval 包含两个 struct timeval 结构体，分别用来指定定时器的间隔时间（interval timer）和初次到期时间（initial expiration time）。
 * old_value：可选参数，如果不为 NULL，则将原来的定时器设置存储在 old_value 所指向的结构体中。
 *
 * 使用 setitimer 可以实现一些重要的功能，例如：
 *  定时器触发信号处理函数：通过设置定时器，在定时器到期时，操作系统会向进程发送指定的信号（如 SIGALRM），进而触发信号处理函数的执行。
 *  实现超时机制：在某些应用场景下，可以使用定时器来实现超时控制，例如网络通信中的超时重传机制，或者在多任务操作系统中的任务调度。
 *  周期性任务调度：通过周期性地设置定时器，可以实现周期性任务的调度和执行，例如定时采集数据、定时刷新界面等。
 *  测量程序运行时间：使用 ITIMER_PROF 定时器类型可以测量程序在用户态和内核态的总运行时间，用于性能分析和优化。
 * */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>
#include <signal.h>

void timeout_handler(int sig) {
    puts("timeout");
    exit(EXIT_FAILURE);
}

int main() {
    struct itimerval timer;

    // 设置定时器间隔为 0（一次性定时器）
    timer.it_interval.tv_sec = 0;
    timer.it_interval.tv_usec = 0;

    // 设置超时时间为 5 秒
    timer.it_value.tv_sec = 5;
    timer.it_value.tv_usec = 0;

    // 注册超时处理函数
    signal(SIGALRM, timeout_handler);

    // 启动定时器
    if (setitimer(ITIMER_REAL, &timer, NULL) == -1) {
        perror("setitimer");
        exit(EXIT_FAILURE);
    }

    // 模拟一个需要时间较长的操作
    printf("Performing some lengthy operation...");
    sleep(10); // 假设这里模拟一个耗时的操作

    // 如果操作未在定时器设置的时间内完成，将会触发超时处理函数
    puts("done");
    return 0;
}
