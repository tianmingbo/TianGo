#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "util/error_out.h"

#define BUF_SIZE 10
#define TRUE 1

/**
 *同时接受多个客户端连接,使用标准IO
 */

int main(int argc, char *argv[]) {
    int serv_sock, cli_sock;
    struct sockaddr_in serv_addr, cli_addr;
    int str_len, option;
    socklen_t cli_addr_size, optlen;
    char message[BUF_SIZE];
    FILE *readfp, *writefp;
    if (argc != 2) {
        printf("Usage: %s <port>\n", argv[0]);
    }
    //创建套接字
    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    if (serv_sock == -1) {
        error_handling("socket() error");
    }

    optlen = sizeof(option);
    option = TRUE;
    //允许立即重用端口。因为主动关闭的一方会进入time_wait状态，确保最后一个 ACK 报文能够被对方正常接收。
    // 等待最长时间为2MSL。MSL表示TCP报文在网络中最长存在时间
    setsockopt(serv_sock, SOL_SOCKET, SO_REUSEADDR, (void *) &option, optlen);

    memset(&serv_addr, 0, sizeof(serv_addr)); //将结构体变量所有成员初始化为0,是为了将sin_zero初始化为0
    serv_addr.sin_family = AF_INET;           //指定地址族
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); //0.0.0.0，要求IP信息是为了明确要从哪个网卡接收数据
    serv_addr.sin_port = htons(atoi(argv[1])); //端口

    //分配ip地址和端口号
    if (bind(serv_sock, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) == -1)
        error_handling("bind() error");

    //调用listen转为可接收请求状态，连接请求等待队列的长度设置为5
    if (listen(serv_sock, 5) == -1)
        error_handling("listen() error");
    else
        printf("start server ip: 0.0.0.0 port: %s\n", argv[1]);
    cli_addr_size = sizeof(cli_addr);
    for (int i = 0; i < 5; ++i) {
        cli_sock = accept(serv_sock, (struct sockaddr *) &cli_addr, &cli_addr_size);
        if (cli_sock == -1)
            error_handling("accept() error");
        else
            printf("cli %d connected\n", i + 1);
        readfp = fdopen(cli_sock, "r"); //把套接字文件描述符转换为标准IO函数中的FILE结构体指针
        writefp = fdopen(cli_sock, "w");
        while (!feof(readfp)) {
            fgets(message, BUF_SIZE, readfp);
            fputs(message, writefp);
            fflush(writefp); //调用fflush将数据立即传输到客户端
        }
        fclose(readfp);
        fclose(writefp);
    }
    close(serv_sock);
    return 0;
}
