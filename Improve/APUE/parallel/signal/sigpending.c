#include "stdio.h"
#include "signal.h"
#include <unistd.h>

static void sig(int no) {
    puts("get SIGINT");
}

int main() {
    signal(SIGINT, sig);
    sigset_t new_mask, old_mask, pend_mask;
    sigemptyset(&new_mask);
    sigaddset(&new_mask, SIGINT);
    puts("block SIGINT");
    sigprocmask(SIG_BLOCK, &new_mask, &old_mask);

    sleep(5);
    //获取未决信号
    sigpending(&pend_mask);
    if (sigismember(&pend_mask, SIGINT)) {
        puts("unblock SIGINT");
        sigprocmask(SIG_SETMASK, &old_mask, NULL);    //恢复
    }

    sleep(5);
    return 0;
}