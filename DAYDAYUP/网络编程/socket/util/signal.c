#include "stdio.h"
#include "unistd.h"
#include "signal.h"

/**
 * void (*signal(int signo, void (*func)(int)))(int);
 * signal 函数接受两个参数，一个是信号编号 signo，一个是一个指向接受 int 参数并返回 void 的函数的指针 func。
 * 然后，signal 函数返回一个函数指针，该函数指针指向一个接受 int 参数并返回 void 的函数。
*/

void timeout(int sig) {
    if (sig == SIGALRM) {
        puts("timeout");
    }
    alarm(2); //每隔两秒产生一次SIGALRM信号
}

void key_control(int sig) {
    if (sig == SIGINT) {
        puts("CTRL_C pressed");
    }
}


int main(void) {
    int i;
    signal(SIGALRM, timeout);
    signal(SIGINT, key_control);
    alarm(2); //2s后发送SIGALRM信号
    for (i = 0; i < 3; i++) {
        puts("wait...");
        sleep(100);//有信号触发后,操作系统会唤醒由于调用sleep而进入阻塞状态的进程.进程一旦被唤醒,就不会再进入睡眠状态
    }
    return 0;
}
