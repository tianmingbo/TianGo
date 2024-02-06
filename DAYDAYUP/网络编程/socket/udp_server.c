#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "util/error_out.h"

#define BUF_SIZE 1024

/**
 * udp server
 * */
int main(int argc, char *argv[]) {
    int serv_sock, str_len;
    struct sockaddr_in serv_addr, cli_addr;
    socklen_t cli_addr_size;
    char message[BUF_SIZE];
    if (argc != 2) {
        printf("Usage: %s <port>\n", argv[0]);
    }
    //创建套接字
    serv_sock = socket(PF_INET, SOCK_DGRAM, 0);
    if (serv_sock == -1) {
        error_handling("socket() error");
    }
    memset(&serv_addr, 0, sizeof(serv_addr)); //将结构体变量所有成员初始化为0,是为了将sin_zero初始化为0
    serv_addr.sin_family = AF_INET;           //指定地址族
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); //0.0.0.0，要求IP信息是为了明确要从哪个网卡接收数据
    serv_addr.sin_port = htons(atoi(argv[1])); //端口

    //分配ip地址和端口号
    if (bind(serv_sock, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) == -1)
        error_handling("bind() error");
    printf("start udp server, port: %s\n", argv[1]);
    while (1) {
        cli_addr_size = sizeof(cli_addr);
        str_len = recvfrom(serv_sock, message, BUF_SIZE, 0,
                           (struct sockaddr *) &cli_addr, &cli_addr_size); //cli_addr是客户端的地址信息
//        printf("%#x\n", cli_addr.sin_addr.s_addr);
        printf("receive data from: %s\n", inet_ntoa(cli_addr.sin_addr));
        sendto(serv_sock, message, str_len, 0, (struct sockaddr *) &cli_addr, cli_addr_size);
    }
    close(serv_sock);
    return 0;
}

