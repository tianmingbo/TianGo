//
// Created by 田明博 on 2024/5/28.
//
/**
 * #include "unistd.h"
 * 复制文件描述符的系统引用,成功返回新的文件描述符,失败返回-1
 * int dup(int oldfd); 复制参数 oldfd 所指向的文件描述符，并返回一个新的文件描述符
 * int dup2(int oldfd. int newfd);也复制文件描述符 oldfd，但是将其复制到指定的文件描述符 newfd 上。如果 newfd 已经打开，则它将首先被关闭，以确保 newfd 引用的是 oldfd 所指向的文件
 * */
#include "stdio.h"
#include "unistd.h"
#include <fcntl.h>
#include "stdlib.h"

#define PATH "/tmp/out"

int main() {
    close(1);
    int fd = open(PATH, O_WRONLY | O_CREAT | O_TRUNC, 0666);
    if (fd < 0) {
        perror("open()");
        exit(1);
    }
//    int new_out = dup(1); //返回当前最小的fd
//    int new2_out = dup2(1, 8);//自己指定最新的fd
    puts("Hello!");
//    printf("new fd :%d\n", new_out);
//    printf("new2_out fd :%d\n", new2_out);
//    write(new_out, "test fd", 7); //输出到stdout
    return 0;
}