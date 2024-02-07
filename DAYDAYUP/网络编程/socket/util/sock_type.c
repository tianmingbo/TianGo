#include <stdio.h>
#include "unistd.h"
#include <netinet/in.h>
#include <netinet/tcp.h>
#include "sys/socket.h"
#include "error_out.h"

/**
 * int getsockopt (int fd, int level, int optname,void *optval,socklen_t * optlen)
 * level要查看的可选项的协议层
 * optname 要查看的可选项名
 * optval 保存结果的地址
 * optlen 保存optval的长度
 *
 * level：
 *   SOL_SOCKET   套接字相关
 *   IPPROTO_IP   IP协议相关
 *   IPPROTO_TCP  TCP协议相关
 * */
int main(int argc, char *argv[]) {
    int tcp_fd, udp_fd;
    int sock_type;
    int no_delay = 1;
    int rcv_buf = 1024 * 3;
    socklen_t optlen;
    int state;
    optlen = sizeof(sock_type);
    tcp_fd = socket(PF_INET, SOCK_STREAM, 0);
    //设置socket
    state = setsockopt(tcp_fd, SOL_SOCKET, SO_RCVBUF, (void *) &rcv_buf, sizeof(rcv_buf));
    if (state)
        error_handling("getsockopt() error");
    printf("res is: %d\n", rcv_buf);
    printf("SOCK_STREAM: %d\n", SOCK_STREAM);

    setsockopt(tcp_fd, IPPROTO_TCP, TCP_NODELAY, (void *) &no_delay, sizeof(no_delay));
    //成功时返回0，失败时返回-1
//    state = getsockopt(tcp_fd, SOL_SOCKET, SO_TYPE, (void *) &sock_type, &optlen); //获取套接字类型
//    state = getsockopt(tcp_fd, SOL_SOCKET, SO_SNDBUF, (void *) &sock_type, &optlen); //输出缓冲区大小
//    state = getsockopt(tcp_fd, SOL_SOCKET, SO_RCVBUF, (void *) &sock_type, &optlen); //输入缓冲区大小
    state = getsockopt(tcp_fd, IPPROTO_TCP, TCP_NODELAY, (void *) &sock_type, &optlen); //禁用Nagle算法？

    if (state)
        error_handling("getsockopt() error");
    printf("res is: %d\n", sock_type);
    return 0;
}
