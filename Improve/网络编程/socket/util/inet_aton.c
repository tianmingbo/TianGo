#include "stdio.h"
#include "arpa/inet.h"
#include "error_out.h"

/**
 * 把ip地址转换为32位网络字节序整型,与inet_addr作用一样
 * */

int main(void) {
    char *addr = "1.2.3.4";
    int res;
    struct sockaddr_in addr_inet;
    res = inet_aton(addr, &addr_inet.sin_addr); //函数自动把结果放入sin_addr中
    if (res)
        printf("Network ordered integer addr: %#x \n", addr_inet.sin_addr.s_addr);
    else
        error_handling("conversion error!");
    return 0;
}

