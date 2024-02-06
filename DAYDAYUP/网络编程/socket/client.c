#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "util/error_out.h"

#define BUF_SIZE 1024

int main(int argc, char *argv[]) {
    int serv_sock;
    struct sockaddr_in serv_addr;
    int recv_len = 0, str_len;
    char message[BUF_SIZE];
    int read_len;
    if (argc != 3) {
        printf("Usage: %s <IP> <port>\n", argv[0]);
    }
    //创建套接字
    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    if (serv_sock == -1) {
        error_handling("socket() error");
    }
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(argv[1]); //将字符串格式的ip地址转换为uint32_t类型
    serv_addr.sin_port = htons(atoi(argv[2]));
    //连接服务器。成功时返回0，失败返回-1
    if (connect(serv_sock, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) == -1)
        error_handling("bind() error");

    while (1) {
        fputs("Input message(Q to quit)", stdout);
        fgets(message, BUF_SIZE, stdin);
        if (!strcmp(message, "q\n") || !strcmp(message, "Q\n"))
            break;
        str_len = write(serv_sock, message, strlen(message));
        read_len = 0;
        while (read_len < str_len) {
            recv_len = read(serv_sock, message, BUF_SIZE - 1);
            if (read_len == -1)
                error_handling("read() error~");
            read_len += recv_len;
        }
        message[recv_len] = 0;
        printf("message from server: %s\n", message);
    }
    close(serv_sock);
    return 0;
}

