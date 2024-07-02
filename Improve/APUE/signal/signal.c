#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

//void (*signal(int signum, void (*handler)(int)))(int);

void handle_signal(int signum) {
    printf("Received signal (%d). Exiting...\n", signum);
    // 在这里添加自定义的信号处理逻辑
    exit(0);
}

int main() {
    // 注册 SIGINT 信号的处理函数
    signal(SIGSEGV, handle_signal);
    signal(SIGUSR1, handle_signal);

    printf("Press Ctrl+C to exit...\n");
    while (1)
        pause();


    return 0;
}