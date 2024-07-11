#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "signal.h"

#define MAXLINE 1024

static void sig_alrm(int s) {
    puts("timeout");
    abort();
}

int main() {
    char *buf[1024];
    signal(SIGALRM, sig_alrm);
    alarm(10);//设置超时10s
    int n = read(0, buf, MAXLINE);
    alarm(0);
    write(1, buf, MAXLINE);
    exit(0);
}
