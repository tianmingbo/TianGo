#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "sys/wait.h"
#include "util/error_out.h"
#include "pthread.h"

#define BUF_SIZE 100
#define MAX_CLI 256
#define TRUE 1

void send_msg(char *msg, int len);

void *handle_cli(void *arg);

pthread_mutex_t mutex;
int cli_cnt = 0; //管理套接字数量
int cli_socks[MAX_CLI]; //管理套接字


/**
 * 多线程并发服务器端
 */

int main(int argc, char *argv[]) {
    int serv_sock, cli_sock;
    struct sockaddr_in serv_addr, cli_addr;
    int option;
    socklen_t cli_addr_size, optlen;
    pthread_t t_id;
    if (argc != 2) {
        printf("Usage: %s <port>\n", argv[0]);
    }
    pthread_mutex_init(&mutex, NULL);

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

    while (1) {
        cli_addr_size = sizeof(cli_addr);
        cli_sock = accept(serv_sock, (struct sockaddr *) &cli_addr, &cli_addr_size);
        if (cli_sock == -1)
            continue;
        pthread_mutex_lock(&mutex);
        cli_socks[cli_cnt++] = cli_sock;
        pthread_mutex_unlock(&mutex);
        pthread_create(&t_id, NULL, handle_cli, (void *) &cli_sock);
        pthread_detach(t_id);//讲线程标记为可分离状态,线程在结束后会自动释放资源
        printf("client connected and ip is: %s \n", inet_ntoa(cli_addr.sin_addr));
    }
}

void *handle_cli(void *arg) {
    int cli_sock = *((int *) arg);
    int str_len, i;
    char msg[BUF_SIZE];
    while ((str_len = read(cli_sock, msg, sizeof(msg))) != 0) {
        printf("recv msg: %s\n", msg);
        send_msg(msg, str_len);
    }
    pthread_mutex_lock(&mutex);
    //断开连接
    for (i = 0; i < cli_cnt; i++) {
        if (cli_sock == cli_socks[i]) {
            while (i++ < cli_cnt - 1)
                cli_socks[i] = cli_socks[i + 1];
            break;
        }
    }
    cli_cnt--;
    printf("cur cli count: %d\n", cli_cnt);
    pthread_mutex_unlock(&mutex);
    close(cli_sock);
    return NULL;
}


void send_msg(char *msg, int len) {
    int i;
    pthread_mutex_lock(&mutex);
    for (i = 0; i < cli_cnt; i++)
        write(cli_socks[i], msg, len);
    pthread_mutex_unlock(&mutex);
}
