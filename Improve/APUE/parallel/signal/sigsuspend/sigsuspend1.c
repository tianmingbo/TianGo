#include "signal.h"
#include "stdio.h"

static void sig_int(int s) {
    puts("get sig_int");
}

int main() {
    sigset_t newmask, oldmask, waitmask;
    puts("start");
    signal(SIGINT, sig_int);
    sigemptyset(&waitmask);
    sigaddset(&waitmask, SIGUSR1);
    sigemptyset(&newmask);
    sigaddset(&newmask, SIGINT);
    sigprocmask(SIG_BLOCK, &newmask, &oldmask);
    puts("临界区");

    sigsuspend(&waitmask); //等同于pause + 允许所有信号，除了sigusr1
    puts("after return from sigsuspend");

    sigprocmask(SIG_SETMASK, &oldmask, NULL);
    puts("end");
    return 0;
}