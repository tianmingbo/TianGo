/**
 * 进程组
 *  pid_t getpgid(pid_t pid);
 *  pid_t getpgrp(void);
 *  int setpgid(pid_t pid, pid_t pgid);
 * */

#include <stdio.h>
#include <unistd.h>

int main() {
    pid_t pgid = getpgrp();

    printf("Process group ID: %d\n", pgid);

    return 0;
}