/**
 * FD_ZERO(fd_set *fdset) 将fdset变量的所有位初始化为0
 * FD_SET(int fd, fd_set *fdset) 从参数fdset指向的变量中注册文件描述符fd的信息
 * FD_CLR(int fd, fd_set *fdset) 从参数fdset指向的变量中清除文件描述符fd的信息
 * FD_ISSET(int fd, fd_set * fdset) fdset指向的变量中是否包含fd的信息
 *
 * */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/select.h>

#define BUF_SIZE 100

void error_handling(char *buf);

int main(int argc, char *argv[]) {
    int serv_sock_fd, cli_sock_fd;
    struct sockaddr_in serv_adr, cli_adr;
    struct timeval timeout;
    fd_set reads, cpy_reads;

    socklen_t adr_sz;
    int fd_max, str_len, fd_num, i;
    char buf[BUF_SIZE];
    if (argc != 2) {
        printf("Usage : %s <port>\n", argv[0]);
        exit(1);
    }

    serv_sock_fd = socket(PF_INET, SOCK_STREAM, 0);
    memset(&serv_adr, 0, sizeof(serv_adr));
    serv_adr.sin_family = AF_INET;
    serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_adr.sin_port = htons(atoi(argv[1]));

    if (bind(serv_sock_fd, (struct sockaddr *) &serv_adr, sizeof(serv_adr)) == -1)
        error_handling("bind() error");
    if (listen(serv_sock_fd, 5) == -1)
        error_handling("listen() error");

    FD_ZERO(&reads);//将fd_set变量的所有位初始化为0
    FD_SET(serv_sock_fd, &reads); //
    fd_max = serv_sock_fd;

    while (1) {
        cpy_reads = reads;
        timeout.tv_sec = 5;
        timeout.tv_usec = 5000;

        /*
         * select()成功时返回大于0的值，失败时返回-1
         * */
        if ((fd_num = select(fd_max + 1, &cpy_reads, 0, 0, &timeout)) == -1)
            //select 失败
            break;

        if (fd_num == 0)
            //无套接字变化
            continue;

        for (i = 0; i < fd_max + 1; i++) {
            //FD_ISSET 查找发生变化的文件描述符
            if (FD_ISSET(i, &cpy_reads)) {
                if (i == serv_sock_fd)     // connection request!服务端套接字发生变化
                {
                    adr_sz = sizeof(cli_adr);
                    cli_sock_fd = accept(serv_sock_fd, (struct sockaddr *) &cli_adr, &adr_sz);
                    FD_SET(cli_sock_fd, &reads); //新建一个与客户端连接的文件描述符
                    if (fd_max < cli_sock_fd)
                        fd_max = cli_sock_fd;
                    printf("connected client: %d \n", cli_sock_fd);
                } else    // read message!
                {
                    str_len = read(i, buf, BUF_SIZE);
                    if (str_len == 0)    // close request!
                    {
                        //接收数据为EOF时需要关闭套接字,并从reads中删除相应信息
                        FD_CLR(i, &reads);
                        close(i);
                        printf("closed client: %d \n", i);
                    } else {
                        write(i, buf, str_len);    // echo!
                    }
                }
            }
        }
    }
    close(serv_sock_fd);
    return 0;
}

void error_handling(char *buf) {
    fputs(buf, stderr);
    fputc('\n', stderr);
    exit(1);
}