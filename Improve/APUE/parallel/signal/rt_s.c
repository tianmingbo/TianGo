/**
 * realtime signal
 * 可以排队,不会丢失
 * */

#include "signal.h"
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"

#define MYRTSIG (SIGRTMIN+6)

static void int_handler(int s) {
    write(1, "!", 1);
}

int main(void) {
    int i;
    sigset_t set, oset, saveset;
    signal(MYRTSIG, int_handler);
    sigemptyset(&set);
    sigaddset(&set, MYRTSIG);
    sigprocmask(SIG_UNBLOCK, &set, &saveset);
    sigprocmask(SIG_BLOCK, &set, &oset);
    while (1) {
        for (i = 0; i < 5; i++) {
            write(1, "*", 1);
            sleep(1);
        }
        write(1, "\n", 1);
        sigsuspend(&oset);
    }
}

