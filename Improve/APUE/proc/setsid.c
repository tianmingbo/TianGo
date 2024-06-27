/**
 * 在父进程中创建子进程时，子进程通常会继承父进程的会话ID（session ID）和进程组ID（process group ID）。
 * 而使用setsid函数可以使调用进程成为一个新的会话领导（session leader），并且不再有控制终端。
 * 具体来说，setsid函数会执行以下几个步骤：
 *  1.如果调用进程不是一个进程组的组长，setsid函数创建一个新的进程组，并将调用进程成为这个新进程组的组长。
 *  2.setsid函数创建一个新的会话（session），并将调用进程分配为这个新会话的会话领导。
 *  3.setsid函数将调用进程的进程组ID设置为与其PID相同，确保调用进程不会再属于任何原始的进程组。
 *  4.setsid函数将当前工作目录切换为根目录，防止守护进程影响当前工作目录的变化。
 * 通过调用setsid函数，守护进程可以独立于终端运行，避免因为终端关闭或者其他终端操作导致的影响。
 * 此外，setsid函数执行成功后，调用进程会和原先的会话组、进程组脱离，获得更高的独立性和隔离性。
 * */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork error");
        exit(1);
    }

    if (pid > 0) {
        // 父进程退出
        exit(0);
    }

    // 子进程继续执行

    // 创建一个新的会话，并成为会话领导
    if (setsid() < 0) {
        perror("setsid error");
        exit(1);
    }

    // 修改当前工作目录为根目录
    if (chdir("/") < 0) {
        perror("chdir error");
        exit(1);
    }

    // 关闭标准输入、标准输出和标准错误
    close(0);
    close(1);
    close(2);

    // 在后台运行
    while (1) {
        // 这里可以添加具体的守护进程任务
        sleep(1);
    }

    return 0;
}