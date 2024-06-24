//
// Created by 田明博 on 2024/6/24.
// fork, exec, wait

#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"

int main() {
    puts("Begin");
    fflush(NULL); //!!!!注意刷新流
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork()");
        exit(1);
    } else if (pid == 0) {
        execl("/bin/date", "date", "+%s", NULL);
        perror("execl()");
        exit(1);
    }
    wait(NULL);
    puts("End!");
    return 0;
}
