//
// Created by 田明博 on 2024/6/3.
// copy实现,fgets

#include "stdlib.h"
#include "stdio.h"

#define BUFSIZE 1024

int main(int argc, char *argv[]) {
    FILE *src, *dest;
    char buf[BUFSIZE];
    if (argc < 3) {
        printf("Usage: %s <src_file> <dest_file>\n", argv[0]);
        exit(1);
    }
    src = fopen(argv[1], "r");
    if (src == NULL) {
        perror("fopen()");
        exit(1);
    }
    dest = fopen(argv[2], "w");
    if (dest == NULL) {
        fclose(src);
        perror("fopen()");
        exit(1);
    }

    while (fgets(buf, BUFSIZE, src) != NULL) {
        fputs(buf, dest);
    }
    fclose(src);
    fclose(dest);
    exit(0);
}
