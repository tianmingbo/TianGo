//
// Created by 田明博 on 2024/6/3.
// copy实现

#include "stdlib.h"
#include "stdio.h"

int main(int argc, char *argv[]) {
    FILE *src, *dest;
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

    while (1) {
        int ch = fgetc(src);
        if (ch == EOF)
            break;
        fputc(ch, dest);
    }
    fclose(src);
    fclose(dest);
    exit(0);
}
