//
// Created by 田明博 on 2024/6/23.
//

#include "unistd.h"
#include "stdio.h"

int main() {

    pid_t p = getpid();
    pid_t pp = getppid();
    printf("pid is: %d\n", p);
    printf("ppid is: %d\n", pp);
    return 0;
}