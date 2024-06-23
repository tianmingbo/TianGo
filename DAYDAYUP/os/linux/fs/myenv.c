//
// Created by 田明博 on 2024/6/22.
//
#include "stdio.h"

extern char **environ;

int main() {
    for (int i = 0; environ[i] != NULL; i++) {
        puts(environ[i]);
    }
    return 0;
}