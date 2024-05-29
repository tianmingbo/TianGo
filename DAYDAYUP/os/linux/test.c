//
// Created by 田明博 on 2024/5/28.
//

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int my_dup2(int oldfd, int newfd) {
    // 如果两个文件描述符相同，直接返回
    if (oldfd == newfd) return newfd;

    // 关闭newfd，以防止覆盖
    close(newfd);

    // 使用dup复制oldfd，并指定为newfd
    int fd = dup(oldfd);
    if (fd == -1) {
        perror("dup");
        exit(EXIT_FAILURE);
    }

    // 如果复制后的文件描述符不是newfd，则关闭之前复制的文件描述符
    if (fd != newfd) close(fd);

    return newfd;
}

int main() {
//    int source_fd = 5;
    int target_fd = 8;
    int source_fd = open("example.txt", O_CREAT | O_RDWR | O_APPEND, 0644);
    // 示例用法
    my_dup2(source_fd, target_fd);
    printf("%d,%d\n", source_fd, target_fd);
    return 0;
}