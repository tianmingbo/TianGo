/**
 * 字节序转换
 * uint16_t htons(uint16_t short);
 * uint16_t ntohs(uint16_t short);
 * uint16_t htonl(uint32_t long);
 * uint16_t ntohl(uint32_t long);
 * htons: h代表主机(host)字节序，n代表网络字节序(network)
 * s是short，2个字节，用于端口转换
 * l是long，4个字节，用于IP地址转换
 * htons是把short型数据从主机字节序转换为网络字节序
 * */

#include "stdio.h"
#include "arpa/inet.h"

int main(int argc, char *argv[]) {
    uint16_t host_port = 8890;
    uint16_t net_port;
    net_port = htons(host_port);
    printf("net_port is: %#x\n", net_port);
    uint32_t host_ip = 0x12345678;
    uint32_t net_ip;
    net_ip = htonl(host_ip);
    printf("net_ip is: %#1x\n", net_ip);
}

