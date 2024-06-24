/**
 * 条件触发(Level-Triggered)
 * */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/epoll.h>

#define BUF_SIZE 4   //减小缓冲区，服务器端一次读取不完接收的数据。因此会多次触发read事件
#define EPOLL_SIZE 50

void error_handling(char *buf);

int main(int argc, char *argv[]) {
    int serv_sock, clnt_sock;
    struct sockaddr_in serv_adr, clnt_adr;

    socklen_t adr_sz;
    int str_len, i;
    char buf[BUF_SIZE];

    struct epoll_event *ep_events;
    struct epoll_event event;
    int epfd, event_cnt;

    if (argc != 2) {
        printf("Usage : %s <port>\n", argv[0]);
        exit(1);
    }

    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    memset(&serv_adr, 0, sizeof(serv_adr));
    serv_adr.sin_family = AF_INET;
    serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
    in_port_t sin_port = htons(atoi(argv[1]));
    serv_adr.sin_port = sin_port;
    printf("start server: %d\n", sin_port);
    if (bind(serv_sock, (struct sockaddr *) &serv_adr, sizeof(serv_adr)) == -1)
        error_handling("bind() error");
    if (listen(serv_sock, 5) == -1)
        error_handling("listen() error");

    epfd = epoll_create(EPOLL_SIZE); //返回epoll的fd
    ep_events = malloc(sizeof(struct epoll_event) * EPOLL_SIZE); //申请文件描述符空间

    event.events = EPOLLIN;
    event.data.fd = serv_sock;
    epoll_ctl(epfd, EPOLL_CTL_ADD, serv_sock, &event); //监听server端fd

    while (1) {
        event_cnt = epoll_wait(epfd, ep_events, EPOLL_SIZE, -1); //成功时返回发生事件的文件描述符数量,失败返回-1
        if (event_cnt == -1) {
            puts("epoll_wait() error");
            break;
        }
        printf("event_cnt: %d\n", event_cnt);
        for (i = 0; i < event_cnt; i++) {
            if (ep_events[i].data.fd == serv_sock) {
                printf("accept event!\n");
                adr_sz = sizeof(clnt_adr);
                clnt_sock = accept(serv_sock, (struct sockaddr *) &clnt_adr, &adr_sz); //建立连接
                event.events = EPOLLIN;
                event.data.fd = clnt_sock;
                epoll_ctl(epfd, EPOLL_CTL_ADD, clnt_sock, &event);
                printf("connected client: %d \n", clnt_sock);
            } else {
                str_len = read(ep_events[i].data.fd, buf, BUF_SIZE);
                printf("read: %s\n", buf);
                if (str_len == 0)    // close request!
                {
                    epoll_ctl(epfd, EPOLL_CTL_DEL, ep_events[i].data.fd, NULL); //删除文件描述符
                    close(ep_events[i].data.fd);
                    printf("closed client: %d \n", ep_events[i].data.fd);
                } else {
                    write(ep_events[i].data.fd, buf, str_len); //echo
                }
            }

        }
    }
    close(serv_sock);
    close(epfd);
    return 0;
}

void error_handling(char *buf) {
    fputs(buf, stderr);
    fputc('\n', stderr);
    exit(1);
}