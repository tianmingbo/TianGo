//
// Created by 田明博 on 2024/6/5.
//
#include "stdlib.h"
#include "stdio.h"
#include "fcntl.h"
#include <unistd.h>

#define BUFSIZE 16*1024

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage error..");
        exit(1);
    }
    int sfd, dfd;
    int n_byte, w_byte;
    char buf[BUFSIZE];
    sfd = open(argv[1], O_RDONLY);
    if (sfd < 0) {
        perror("open()");
        exit(1);
    }
    dfd = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (dfd < 0) {
        close(sfd);
        perror("open()");
        exit(1);
    }
    while (1) {
        n_byte = read(sfd, buf, BUFSIZE);
        if (n_byte < 0) {
            perror("read()");
            break;
        }
        if (n_byte == 0)
            break;
        w_byte = 0;
        while (w_byte < n_byte) {
            w_byte = write(dfd, buf, n_byte);
            if (w_byte < 0) {
                perror("read()");
                break;
            }
        }

    }
    close(sfd);
    close(dfd);
    return 0;
}
