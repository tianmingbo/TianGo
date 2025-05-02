#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BUFSIZE 1024

int main() {
    pid_t pid;
    int pd[2];
    char str[BUFSIZE];

    if (pipe(pd) < 0) {
        perror("pipe");
        exit(1);
    }
    if ((pid = fork()) < 0) {
        perror("fork");
        exit(1);
    }
    if (pid > 0) {
        close(pd[0]); //parent
        write(pd[1], "hello world\n", 12);
        close(pd[1]);
        wait(NULL);
    } else {
        close(pd[1]); //child
        read(pd[0], &str, BUFSIZE);
        puts(str);
        close(pd[0]);
        exit(0);
    }
    return 0;
}
