//
// Created by 田明博 on 2024/6/25.
// 切换real, effective, save用户ID或组ID. 前提是拥有 有效用户ID 或 有效组ID
#include "stdlib.h"
#include "stdio.h"
#include "unistd.h"

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage...");
        exit(1);
    }
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork()");
        exit(1);
    }
    if (pid == 0) {
        setuid(atoi(argv[1]));
        execvp(argv[2], argv + 2);
        perror("execvp()");
        exit(1);
    }
    wait(NULL);
    return 0;
}