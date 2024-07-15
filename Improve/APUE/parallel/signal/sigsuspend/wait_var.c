#include <stdio.h>
#include <signal.h>
#include <unistd.h>

volatile sig_atomic_t quitflag;

static void sig_handler(int s) {
    if (s == SIGINT)
        printf("\ninterrupt\n");
    else if (s == SIGQUIT) {
        printf("\nquit\n");
        quitflag = 1;
    }
}

int main() {
    printf("%d\n", getpid());
    sigset_t newmask, oldmask, zeromask;
    signal(SIGINT, sig_handler);
    signal(SIGQUIT, sig_handler);

    sigemptyset(&zeromask);
    sigemptyset(&newmask);
    sigaddset(&newmask, SIGQUIT);

    sigprocmask(SIG_BLOCK, &newmask, &oldmask);

    while (quitflag == 0) //替换信号mask，什么信号都不屏蔽，有机会使QUIT信号生效
        sigsuspend(&zeromask);

    quitflag = 0;

    sigprocmask(SIG_SETMASK, &oldmask, NULL);
    return 0;

}
