#include "stdio.h"
#include "stdlib.h"
#include <pwd.h>
#include <signal.h>
#include <unistd.h>
#include "string.h"

static void my_alarm(int signo) {
    struct passwd *rootptr;
    printf("in signal handler\n");
    if ((rootptr = getpwnam("root")) == NULL)
        puts("getpwnam(root) error");
    alarm(1);
}

int main(void) {

    struct passwd *ptr;
    signal(SIGALRM, my_alarm);
    alarm(1);
    for (;;) {
        if ((ptr = getpwnam("sar")) == NULL)
            puts("getpwnam error");
        if (strcmp(ptr->pw_name, "sar") != 0)
            printf("return value corrupted!, pw_name =%s\n", ptr->pw_name);
    }
}
