#include "stdio.h"
#include "arpa/inet.h"
#include "string.h"

/**
 * 将整数型ip转换为字符串格式
 * */

int main(void) {
    uint32_t n = 0x4030201;
    char *str_ptr;
    char str_arr[20];
    struct sockaddr_in addr1;
    addr1.sin_addr.s_addr = htonl(n);
    str_ptr = inet_ntoa(addr1.sin_addr); //成功时返回转换的字符串地址值，失败返回-1
    strcpy(str_arr, str_ptr);
    printf("res is: %s \n", str_arr);
    return 0;
}

