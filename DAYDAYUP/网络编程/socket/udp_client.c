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
    int str_len;
    char message[BUF_SIZE];
    socklen_t adr_size;
    if (argc != 3) {
        printf("Usage: %s <IP> <port>\n", argv[0]);
    }
    //创建套接字
    serv_sock = socket(PF_INET, SOCK_DGRAM, 0);
    if (serv_sock == -1) {
        error_handling("socket() error");
    }
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(argv[1]); //将字符串格式的ip地址转换为uint32_t类型
    serv_addr.sin_port = htons(atoi(argv[2]));

    while (1) {
        fputs("Input message(Q to quit)", stdout);
        fgets(message, BUF_SIZE, stdin);
        if (!strcmp(message, "q\n") || !strcmp(message, "Q\n"))
            break;
        //调用sendto函数时自动分配IP和端口号
        sendto(serv_sock, message, strlen(message), 0,
               (struct sockaddr *) &serv_addr, sizeof(serv_addr));
        adr_size = sizeof(serv_addr);
        str_len = recvfrom(serv_sock, message, BUF_SIZE, 0,
                           (struct sockaddr *) &serv_addr, &adr_size); //serv_addr保存发送者的信息
        printf("receive from: %s\n", inet_ntoa(serv_addr.sin_addr));
        message[str_len] = 0;
        printf("message from server: %s\n", message);
    }
    close(serv_sock);
    return 0;
}

