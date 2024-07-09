/**
 * int sigprocmask(int how, const sigset_t *set, sigset_t *oldset);
 * how: 指定对信号掩码的操作方式,可取以下值:
 *   SIG_BLOCK: 将信号集 set 中的信号添加到当前进程的信号掩码中。
 *   SIG_UNBLOCK: 从当前进程的信号掩码中移除信号集 set 中的信号。
 *   SIG_SETMASK: 将当前进程的信号掩码设置为信号集 set。
 * set: 要设置的信号集。可以为 NULL。
 * oldset: 用于保存当前进程的信号掩码。可以为 NULL。
 * */
#include "stdio.h"
#include "signal.h"
#include <unistd.h>


int main() {
    sigset_t new_mask, old_mask;
    sigemptyset(&new_mask);
    sigaddset(&new_mask, SIGINT);
    puts("block SIGINT");
    sigprocmask(SIG_BLOCK, &new_mask, &old_mask);

    sleep(5);
    //恢复
    puts("unblock SIGINT");
    sigprocmask(SIG_SETMASK, &old_mask, NULL);
    sleep(5);
    return 0;
}

