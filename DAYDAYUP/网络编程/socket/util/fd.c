#include "stdio.h"
#include "fcntl.h"
#include "unistd.h"
#include "sys/socket.h"

/**
 * 文件描述符:
 * 0:标准输入
 * 1:标准输出
 * 2:标准错误
 * 程序开始后, 0,1,2自动分配
*/
int main(void) {
    int fd1, fd2, fd3;
    fd1 = socket(PF_INET, SOCK_STREAM, 0); //套接字也是一个文件描述符
    fd2 = open("hello_client.c", O_RDONLY);
    fd3 = socket(PF_INET, SOCK_DGRAM, 0);
    printf("fd1: %d\n", fd1); //3
    printf("fd2: %d\n", fd2); //4
    printf("fd3: %d\n", fd3); //5
    close(fd1);
    close(fd2);
    close(fd3);
    return 0;
}
