/**
 * int sigaction(int signum, const struct sigaction *act, struct sigaction *oldact);
 *      signum: 要设置处理程序的信号编号。可以使用诸如 SIGINT、SIGTERM 等宏定义的信号编号。
 *      act: 指向 sigaction 结构体的指针,用于设置新的信号处理程序。如果该参数为 NULL,则只获取当前的信号处理程序。
 *      oldact: 如果不为 NULL,则返回先前设置的信号处理程序信息。
 *
 * struct sigaction {
    void (*sa_handler)(int); // 信号处理函数指针
    sigset_t sa_mask; // 在信号处理函数执行期间需要被阻塞的信号集合
    int sa_flags; // 控制信号处理行为的标志位
    void (*sa_sigaction)(int, siginfo_t *, void *); // 可选的信号处理函数指针
};
 *
 * sa_handler: 指向信号处理函数的函数指针。
 * sa_mask: 在信号处理函数执行期间需要被阻塞的信号集合。
 * sa_flags: 控制信号处理行为的标志位,如 SA_SIGINFO 表示使用扩展的信号处理函数 sa_sigaction。
 * sa_sigaction: 可选的扩展信号处理函数指针,提供了更多信号信息。
 * */
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

void my_sigaction(int signum, siginfo_t *info, void *ucontext) {
    printf("Received signal %d from pid %d\n", signum, info->si_pid);
    // 在此处实现自定义的信号处理逻辑
}

int main() {
    struct sigaction act;
    act.sa_flags = SA_SIGINFO;
    act.sa_sigaction = my_sigaction;
    sigaction(SIGINT, &act, NULL);

    while (1) {
        printf("Waiting for SIGINT...\n");
        pause();
    }

    return 0;
}
