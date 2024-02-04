#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

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
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(atoi(argv[1]));

    //分配ip地址和端口号
    if (bind(serv_sock, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) == -1)
        error_handling("bind() error");
    //调用listen转为可接收请求状态
    if (listen(serv_sock, 5) == -1)
        error_handling("listen() error");

    cli_addr_size = sizeof(cli_addr);
    //受理连接请求
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