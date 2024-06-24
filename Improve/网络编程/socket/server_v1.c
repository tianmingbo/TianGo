#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

/**
 *只接受一次客户端连接
 */
void error_handling(char *buf);

int main(int argc, char *argv[]) {
    int serv_sock, cli_sock;
    struct sockaddr_in serv_addr, cli_addr;
    socklen_t cli_addr_size;
    char message[] = "hello world;\n";
    if (argc != 2) {
        printf("Usage: %s <port>\n", argv[0]);
    }
    //创建套接字
    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
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
    //调用listen转为可接收请求状态，连接请求等待队列的长度设置为5
    if (listen(serv_sock, 5) == -1)
        error_handling("listen() error");

    cli_addr_size = sizeof(cli_addr);
    //受理连接请求,成功时返回创建的套接字文件描述符。自动创建套接字，并连接到发起请求的客户端
    cli_sock = accept(serv_sock, (struct sockaddr *) &cli_addr, &cli_addr_size);
    if (cli_sock == -1) {
        error_handling("accept() error");
    }
    //传输数据
    write(cli_sock, message, sizeof(message));
    close(cli_sock);
    close(serv_sock);
    return 0;
}

void error_handling(char *buf) {
    fputs(buf, stderr);
    fputc('\n', stderr);
    exit(1);
}