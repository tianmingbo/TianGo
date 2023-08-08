#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/select.h>

#define BUF_SIZE 30

int main() {
    fd_set reads, temps; //reads是否存在待读取数据的文件描述符
    int result, str_len;
    char buf[BUF_SIZE];
    struct timeval timeout;
    FD_ZERO(&reads);
    FD_SET(0, &reads);
    while (1) {
        temps = reads; //temps保存初始值，因为调用select后，除了发生变化的文件描述符对应位外，其它都会置零
        timeout.tv_sec = 5;
        timeout.tv_usec = 0;
        result = select(1, &temps, 0, 0, &timeout); //返回值是发生变化的文件描述符的数量
        printf("%d\n", result);
        if (result == -1) {
            puts("select() error");
            break;
        } else if (result == 0) {
            puts("timeout");
        } else {
            if (FD_ISSET(0, &temps)) {
                str_len = read(0, buf, BUF_SIZE);
                buf[str_len] = 0;
                printf("message from console:%s", buf);
            }
        }
    }
    return 0;
}