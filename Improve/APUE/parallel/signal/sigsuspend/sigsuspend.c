/**
 * sigsuspend() 用于 暂时 替换进程的信号掩码并挂起进程,直到收到指定的信号。函数的作用如下:

将进程的信号掩码临时替换为 mask 参数指定的信号掩码。
挂起进程的执行,直到收到一个未被屏蔽的信号。
当收到信号时,将信号掩码恢复为调用 sigsuspend() 之前的状态。
返回信号处理函数的返回值。如果信号处理函数返回,则 sigsuspend() 返回 -1，并将 errno 设置为 EINTR。
 * */
#include "signal.h"
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"

static void int_handler(int s) {
    write(1, "!", 1);
}

int main(void) {
    int i;
    sigset_t set, oset, saveset;
    signal(SIGINT, int_handler);
    sigemptyset(&set);
    sigaddset(&set, SIGINT);
    sigprocmask(SIG_UNBLOCK, &set, &saveset);
    sigprocmask(SIG_BLOCK, &set, &oset);
    while (1) {
        for (i = 0; i < 5; i++) {
            write(1, "*", 1);
            sleep(1);
        }
        write(1, "\n", 1);
        sigsuspend(&oset);
//        sigprocmask(SIG_SETMASK, &oset, NULL); 极限一点，在还没执行到pause的时候，按了^C，这时候就在pause永远阻塞了。因为这个和pause不是原子操作。
//        pause();
    }
    sigprocmask(SIG_SETMASK, &saveset, NULL);
    exit(0);
}

