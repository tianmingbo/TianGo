/**
 * 进程间同步，父进程先执行
 * */

#include "signal.h"
#include "unistd.h"
#include "stdio.h"
#include "stdlib.h"

static volatile sig_atomic_t sigflag;
static sigset_t newmask, oldmask, zeromask;

static void sig_usr(int s) {
    sigflag = 1;
}

void tell_wait() {
    signal(SIGUSR1, sig_usr);

    sigemptyset(&newmask);
    sigemptyset(&zeromask);
    //屏蔽SIGUSR1和SIGUSR2信号
    sigaddset(&newmask, SIGUSR1);
    sigaddset(&newmask, SIGUSR2);

    sigprocmask(SIG_BLOCK, &newmask, &oldmask);//阻塞SIGUSR1和SIGUSR2
}

void tell_parent(pid_t pid) {
    kill(pid, SIGUSR2);
}

void wait_parent() {
    while (sigflag == 0)
        sigsuspend(&zeromask); //暂时什么都不屏蔽,等待一个信号
    sigflag = 0;
    sigprocmask(SIG_SETMASK, &oldmask, NULL);

}

void tell_child(pid_t pid) {
    kill(pid, SIGUSR1);
}

void wait_child() {
    while (sigflag == 0)
        sigsuspend(&zeromask);
    sigflag = 0;
    sigprocmask(SIG_SETMASK, &oldmask, NULL);
}

static void charatatime(char *str) {
    char a;
    setbuf(stdout, NULL);//设置无缓冲区
    for (; (a = *str++) != 0;) {
        putc(a, stdout);
    }
}

int main() {
    pid_t pid;
    tell_wait();
    pid = fork();
    if (pid < 0)
        exit(1);
    if (pid == 0) {
        wait_parent();
        charatatime("child\n");
//        tell_parent(getppid());
    } else {
//        wait_child();
        charatatime("parent\n");
        tell_child(pid);
    }
    return 0;
}