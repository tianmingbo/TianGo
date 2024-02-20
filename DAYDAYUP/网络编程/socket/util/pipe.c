/**
 * 进程通信（pipe）
 * int pipe(int pipedes[2])
 * pipedes[0] 通过管道接收数据时使用的文件描述符，即管道出口
 * pipedes[1] 通过管道传输数据时使用的文件描述符，即管道入口
 * */

#include "stdio.h"
#include "unistd.h"

#define BUF_SIZE 30


int main(int argc, char *argv[]) {
    int fds1[2], fds2[2];
    char str1[] = "Who are you";
    char str2[] = "tian";
    char buf[BUF_SIZE];
    pid_t pid;

    pipe(fds1);
    pipe(fds2);
    pid = fork();
    if (pid == 0) {
        write(fds1[1], str1, sizeof(str1));
        read(fds2[0], buf, BUF_SIZE);
        printf("child proc output: %s \n", buf);
    } else {
        read(fds1[0], buf, BUF_SIZE);
        printf("parent proc output: %s \n", buf);
        write(fds2[1], str2, sizeof(str1));
        sleep(3);
    }
    return 0;
}