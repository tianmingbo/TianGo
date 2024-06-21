//
// Created by 田明博 on 2024/6/17.
// 目录读取
#include <stdio.h>
#include <glob.h>
#include "string.h"

int err_func(const char *errpath, int errno) {
    puts(errpath);
    fprintf(stderr, "ERROR msg:%s\n", strerror(errno));
    return 0;
}

int main() {
    glob_t glob_result;
    int return_value = glob("/etc/*", 0, err_func, &glob_result);
    //0 success
    if (return_value == 0) {
        for (size_t i = 0; i < glob_result.gl_pathc; ++i) {
            puts(glob_result.gl_pathv[i]);
        }

        globfree(&glob_result);
    } else {
        printf("Error in glob function.\n");
    }

    return 0;
}