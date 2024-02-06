#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "util/error_out.h"

#define BUF_SIZE 1024

int main(int argc, char *argv[]) {
    int serv_sock, read_cnt;
    struct sockaddr_in serv_addr;
    FILE *fp;
    char buf[BUF_SIZE];
    fp = fopen("tmp.txt", "wb");
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

    while ((read_cnt = read(serv_sock, buf, BUF_SIZE)) != 0)
        fwrite((void *) buf, 1, read_cnt, fp);
    puts("received file data");
    write(serv_sock, "Thank you", 10);
    fclose(fp);
    close(serv_sock);
    return 0;
}

