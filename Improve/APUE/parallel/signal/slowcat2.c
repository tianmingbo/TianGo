//
// Created by 田明博 on 2024/7/9.
// 令牌桶
/**
 * 实现一个复制文本到标准输出的程序，要求10字符10字符的复制，且不能让CPU空转。
 * */
#include "stdlib.h"
#include "stdio.h"
#include "signal.h"
#include "errno.h"
#include "unistd.h"
#include <fcntl.h>

#define CPS 10
#define BUFSIZE CPS
#define BUCKET 100 //桶容量

static volatile int token = 0;

static void alrm_handler(int s) {
    alarm(1);
    token = token > BUCKET ? BUCKET : token + 1;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        puts("Usage err..");
        exit(1);
    }
    char buf[BUFSIZE];
    int sfd, dfd = 1;
    ssize_t len, pos, ret;
    signal(SIGALRM, alrm_handler);
    alarm(1);
    do {
        if ((sfd = open(argv[1], O_RDONLY)) < 0) {
            if (errno != EINTR) {
                perror("open()");
                exit(1);
            }
        }
    } while (sfd < 0);
    while (1) {
        while (token <= 0)
            pause();
        token--;
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
