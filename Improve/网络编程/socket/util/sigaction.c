#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "signal.h"
#include "sys/wait.h"

/**
 * 类似signal
 * int sigaction (int sig, const struct sigaction * act, struct sigaction * oact)
 *
*/


void handleSignal(int signal) {
    int status;
    pid_t id = waitpid(-1, &status, WNOHANG);//等待子进程结束
    if (WIFEXITED(status)) {
        printf("removed prod id: %d \n", id);
        printf("child send: %d\n", WEXITSTATUS(status));
    }
}

int main() {
    pid_t pid;
    struct sigaction sa;
    sa.sa_handler = handleSignal;
    sa.sa_flags = 0;
    sigemptyset(&sa.sa_mask);
    //当父进程接收到 SIGCHLD 信号时，在 handleSignal 函数中调用 waitpid 函数获取子进程的退出状态，并使用 WIFEXITED 和 WEXITSTATUS 宏来判断子进程是否正常退出，并打印相应的信息。
    sigaction(SIGCHLD, &sa, NULL);
    pid = fork();

    if (pid == 0) {
        // 这是子进程
        printf("子进程1\n");
        sleep(10);
        return 666;
    } else {
        printf("我是父进程,子进程id：%d\n", pid);
        pid = fork();
        if (pid == 0) {
            printf("子进程2\n");
            sleep(20);
            exit(123);
        } else {
            int i;
            printf("子进程id：%d\n", pid);
            for (i = 0; i < 5; i++) {
                puts("wait...");
                sleep(5);
            }
        }
    }

    return 0;
}