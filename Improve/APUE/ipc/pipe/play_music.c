/**
 * mp3解析,父进程读取,子进程解析
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#define BUFSIZE 1024

int main(const int argc, char **argv) {
    if (argc != 2) {
        printf("Usage: %s <file>\n", argv[0]);
        exit(1);
    }
    int pd[2];
    const char *path = argv[1];
    if (pipe(pd) < 0) {
        perror("pipe");
        exit(1);
    }
    const pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        exit(1);
    }
    if (pid == 0) {
        //child
        close(pd[1]);
        dup2(pd[0], 0); //重定向到标准输入
        close(pd[0]);
        const int fd = open("/dev/null", O_RDWR);
        dup2(fd, 1); //不希望有输出
        dup2(fd, 2);
        // - 是接收标准输入
        execl("/usr/local/bin/mpg123", "mpg123", "-",NULL);
        perror("execl");
        exit(0);
    }

    //parent
    close(pd[0]);
    const int fd = open(path, O_RDONLY);
    char buf[BUFSIZE];
    if (fd < 0) {
        perror("open");
        exit(1);
    }
    size_t bytes;
    while ((bytes = read(fd, buf,BUFSIZE)) > 0) {
        if (write(pd[1], buf, bytes) != bytes) {
            perror("write to pipe failed!");
            exit(1);
        }
    }
    close(fd);
    close(pd[1]);
    wait(NULL); //等待子进程退出
    return 0;
}
