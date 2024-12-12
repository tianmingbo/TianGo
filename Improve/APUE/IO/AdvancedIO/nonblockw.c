#include <stdio.h>
#include "fcntl.h"
#include "unistd.h"
#include "stdlib.h"
#include "errno.h"

char buf[50000];

int main() {
    int n_to_write, n_write;
    int fd1, fd2;
    char *ptr;
    fd1 = fcntl(STDIN_FILENO, F_GETFL);
    n_to_write = read(STDIN_FILENO, buf, 50000);
    printf("read %d bytes\n", n_to_write);
    fcntl(STDIN_FILENO, F_SETFL, fd1 | O_NONBLOCK); //set nonblock
    ptr = buf;
    while (n_to_write > 0) {
        errno = 0;
        n_write = write(STDOUT_FILENO, ptr, n_to_write);
        fprintf(stderr, "n_write = %d, errno = %d\n", n_write, errno);

        if (n_write > 0) {
            ptr += n_write;
            n_to_write -= n_write;
        }
    }
    fcntl(STDIN_FILENO, F_SETFL, fd1); //clear nonblock
    exit(0);
}