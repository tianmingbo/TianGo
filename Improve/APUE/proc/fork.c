//
// Created by 田明博 on 2024/6/23.
//

#include "stdio.h"
#include "unistd.h"
#include "stdlib.h"

int main() {

    pid_t pid;
    printf("[%d] begin()\n", getpid());
    fflush(NULL); //******* 刷新流
    pid = fork();
    if (pid < 0) {
        perror("fork()");
        exit(1);
    }
    if (pid == 0) {
        printf("[%d] sub is running!\n", getpid());
    } else {
        printf("[%d] parent is running!\n", getpid());
    }
    printf("[%d] end\n", getpid());
    return 0;
}