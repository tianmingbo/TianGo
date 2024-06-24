//
// Created by 田明博 on 2024/6/23.
// fork,wait
#include "stdlib.h"
#include "stdio.h"
#include "unistd.h"
#include <sys/wait.h>

#define LEFT 30000000
#define RIGHT 30000200

int main() {
    pid_t pid;
    int i, j, mark;
    for (i = LEFT; i < RIGHT; i++) {
        pid = fork();
        if (pid < 0) {
            perror("fork()");
            exit(1);
        }
        if (pid == 0) {
            mark = 1;
            for (j = 2; j < i / 2; j++) {
                if (i % j == 0) {
                    mark = 0;
                    break;

                }
            }
            if (mark)
                printf("%d is a primer\n", i);
            exit(0);
        }
    }
    for (i = LEFT; i <= RIGHT; i++) {
        wait(NULL);
    }
    return 0;
}
