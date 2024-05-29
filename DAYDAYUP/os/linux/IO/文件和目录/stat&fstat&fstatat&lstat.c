//
// Created by 田明博 on 2024/5/29.
//
/**
 * #include <sys/types.h>
 * #include <sys/stat.h>
 * #include <fcntl.h>
 * int stat(const char *path, struct stat *buf); 用于获取指定路径下文件的状态信息，需要传入文件路径作为参数。
 * int fstat(int fd, struct stat *buf); 获取文件描述符所指向的文件的状态信息，需要传入文件描述符作为参数。
 * int fstatat(int fd, const char *pathname, struct stat *buf, int flags); 类似于stat()，但可以指定相对路径和基准目录，避免了一些路径问题。
 * int lstat(const char *path, struct stat *buf); 类似于stat()，但对于符号链接会返回链接本身的信息，而不是链接指向的文件的信息。
 *
 * 返回的结构体（比如struct stat）中包含了诸如文件大小、修改时间、权限等信息。
 * */
#include <sys/fcntl.h>
#include "apue.h"

int main() {
    const char *file_path = "example.txt";
    struct stat file_info;

    // 获取文件状态信息
    if (stat(file_path, &file_info) == 0) {
        printf("File size: %lld bytes\n", file_info.st_size);
        printf("File permissions: %o\n", file_info.st_mode & 0777); // 权限以八进制形式表示
        // 其他信息也可以在file_info中找到
    } else {
        perror("stat");
    }
    printf("******************************************\n");
    int fd = open(file_path, O_RDONLY);
    // 获取文件状态信息
    if (fstat(fd, &file_info) == 0) {
        printf("File size: %lld bytes\n", file_info.st_size);
        printf("File permissions: %o\n", file_info.st_mode & 0777);
        // 其他信息也可以在file_info中找到
    } else {
        perror("stat");
    }
    printf("******************************************\n");
    const char *relative_path = "example.txt";
    int base_directory = AT_FDCWD; // 指定当前工作目录

    // 获取相对路径文件的状态信息
    if (fstatat(base_directory, relative_path, &file_info, 0) == 0) {
        printf("File size: %lld bytes\n", file_info.st_size);
        printf("File permissions: %o\n", file_info.st_mode & 0777);
        // 其他信息也可以在file_info中找到
    } else {
        perror("fstatat");
    }
    return 0;
}