//
// Created by 田明博 on 2024/7/9.
// 漏桶,漏桶算法(Leaky Bucket)是网络世界中流量整形（Traffic Shaping）或速率限制（Rate Limiting）时经常使用的一种算法，
// 它的主要目的是控制数据注入到网络的速率，平滑网络上的突发流量。
/**
 * 实现一个复制文本到标准输出的程序，要求10字符10字符的复制，且不能让CPU空转。
 * */
#include "stdlib.h"
#include "stdio.h"
#include "signal.h"
#include "errno.h"
#include "unistd.h"
#include <fcntl.h>
#include <sys/time.h>

#define CPS 10
#define BUFSIZE CPS

static volatile int loop = 0;

static void alrm_handler(int s) {
//    alarm(1);
    loop = 1;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        puts("Usage err..");
        exit(1);
    }
    struct itimerval timer;

    char buf[BUFSIZE];
    int sfd, dfd = 1;
    ssize_t len, pos, ret;
    signal(SIGALRM, alrm_handler);
    timer.it_interval.tv_sec = 1; //1s 1次
    timer.it_interval.tv_usec = 0;
    timer.it_value.tv_sec = 1;
    timer.it_value.tv_usec = 0;
    // 启动定时器
    if (setitimer(ITIMER_REAL, &timer, NULL) == -1) {
        perror("setitimer()");
        exit(EXIT_FAILURE);
    }
//    alarm(1);
    do {
        if ((sfd = open(argv[1], O_RDONLY)) < 0) {
            if (errno != EINTR) {
                perror("open()");
                exit(1);
            }
        }
    } while (sfd < 0);
    while (1) {
        while (!loop)
            pause();
        loop = 0;
        while ((len = read(sfd, buf, BUFSIZE)) < 0) {
            if (errno != EINTR) {
                perror("read()");
                break;
            }
        }
        if (len == 0)
            break;
        pos = 0;
        while (len > 0) {
            if ((ret = write(dfd, buf + pos, len)) < 0) {
                if (errno == EINTR)
                    continue;
                perror("write()");
                exit(1);
            }
            pos += ret;
            len -= ret;
        }
    }
    close(sfd);
    return 0;
}
