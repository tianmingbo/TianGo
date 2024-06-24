//
// Created by 田明博 on 2024/5/15.
// 使用fgets
//

#include "stdio.h"

#define SLEN 10

int main() {
    char words[SLEN];
    puts("Enter a string(q to quit):");
    while (fgets(words, SLEN, stdin) != NULL && words[0] != 'q') {
        int i = 0;
        while (words[i] != '\n' && words[i] != '\0')
            i++;
        if (words[i] == '\n')
            words[i] = '\0';
        else
            while (getchar() != '\n')
                continue;
        puts(words);
    }
    puts("done");
    return 0;
}