/**
 * 基于半关闭的文件传输server
 * shutdown(int sock, int howto)
 * SHUT_RD 断开输入流，套接字无法接收数据
 * SHUT_WR 断开输出流，无法传输数据，但是缓冲区的未传输数据会继续传输
 * SHUT_RDWR 同时断开IO流
 * */
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "unistd.h"
#include "arpa/inet.h"
#include "sys/socket.h"
#include "util/error_out.h"

#define BUF_SIZE 30

int main(int argc, char *argv[]) {
    int serv_sd, cli_sd;
    FILE *fp;
    char buf[BUF_SIZE];
    int read_cnt;

    struct sockaddr_in serv_addr, cli_addr;
    socklen_t cli_addr_sz;

    if (argc != 2) {
        error_handling("para error!");
        exit(1);
    }

    fp = fopen("file_server.c", "rb");
    serv_sd = socket(PF_INET, SOCK_STREAM, 0);

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(atoi(argv[1]));

    bind(serv_sd, (struct sockaddr *) &serv_addr, sizeof(serv_addr));
    listen(serv_sd, 5);

    cli_addr_sz = sizeof(cli_addr);
    cli_sd = accept(serv_sd, (struct sockaddr *) &cli_addr, &cli_addr_sz);

    while (1) {
        read_cnt = fread((void *) buf, 1, BUF_SIZE, fp);
        if (read_cnt < BUF_SIZE) {
            write(cli_sd, buf, read_cnt);
            break;
        }
        write(cli_sd, buf, BUF_SIZE);
    }
    shutdown(cli_sd, SHUT_WR);//关闭输出流
    read(cli_sd, buf, BUF_SIZE);//依然可以通过输入流读取数据
    printf("receive from cli: %s\n", buf);

    fclose(fp);
    close(cli_sd);
    close(serv_sd);
    return 0;
}