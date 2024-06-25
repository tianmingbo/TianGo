//
// Created by 田明博 on 2024/6/25.
// 解释器文件

#include "stdio.h"
#include "unistd.h"
#include "stdlib.h"
#include <sys/wait.h>

int main() {
    pid_t pid = fork();
    if (pid == 0) {
        execl("./interpreter_file.py", "test", "p1", "p2", NULL);
        perror("execl");
        exit(1);
    } else
        wait(NULL);
    return 0;
}
