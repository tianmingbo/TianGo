#include "stdio.h"
#include "arpa/inet.h"

/**
 * 把ip地址转换为32位网络字节序整型
 * */
int main(void) {
    char *addr = "1.2.3.4";
    char *add2 = "192.168.109.1211";
    uint32_t conv_addr = inet_addr(addr);
    if (conv_addr == INADDR_NONE)
        printf("Error conv!\n");
    else
        printf("Network ordered integer addr: %#1x \n", conv_addr);
    uint32_t conv_addr2 = inet_addr(add2);
    if (conv_addr2 == INADDR_NONE)
        printf("Error conv!\n");
    else
        printf("Network ordered integer addr: %#1x \n", conv_addr2);

    return 0;
}
