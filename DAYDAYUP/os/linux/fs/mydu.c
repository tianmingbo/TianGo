//
// Created by 田明博 on 2024/6/19.
// du实现
#include "stdio.h"
#include "stdlib.h"
#include "sys/stat.h"
#include <glob.h>
#include "string.h"

#define MAX_PATH_LEN 1024

static int64_t mydu(const char *);

int main(int argc, char **argv) {
    if (argc < 2) {
        puts("Usage...");
        exit(1);
    }
    printf("%lld\n", mydu(argv[1]) / 2);
    return 0;
}


static int64_t mydu(const char *pathname) {
    int64_t sum;
    char *pos;
    static struct stat file_info;
    static char next_path[MAX_PATH_LEN];
    glob_t glob_result;

    if (lstat(pathname, &file_info) < 0) {
        perror("lstat()");
        exit(1);
    }
    if (!S_ISDIR(file_info.st_mode)) {
        return file_info.st_blocks;
    }
    strncpy(next_path, pathname, MAX_PATH_LEN);
    strncat(next_path, "/*", MAX_PATH_LEN);
    glob(next_path, 0, NULL, &glob_result);

    strncpy(next_path, pathname, MAX_PATH_LEN);
    strncat(next_path, "/.*", MAX_PATH_LEN);
    glob(next_path, GLOB_APPEND, NULL, &glob_result);

    sum = file_info.st_blocks;

    for (size_t i = 0; i < glob_result.gl_pathc; i++) {
        pos = strrchr(glob_result.gl_pathv[i], '/');
        if (strcmp(pos + 1, ".") == 0 || strcmp(pos + 1, "..") == 0)
            continue;
        sum += mydu(glob_result.gl_pathv[i]);
    }
    globfree(&glob_result);
    return sum;
}

