//
// Created by 田明博 on 2024/5/15.
// 使用fgets和fputs
//

#include "stdio.h"

#define SLEN 14

int main() {
    char words[SLEN];
    puts("Enter a string(q to quit):");
    while (fgets(words, SLEN, stdin) != NULL && words[0] != 'q')
        fputs(words, stdout);
    puts("done");
    return 0;
}