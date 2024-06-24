#include "stdio.h"
#include "arpa/inet.h"
#include "netdb.h"
#include "error_out.h"

/**
 * 根据域名获取ip地址
*/
int main(int argc, char *argv[]) {
    int i;
    struct hostent *host;
    if (argc != 2) {
        error_handling("error para");
        exit(1);
    }
    host = gethostbyname(argv[1]);
    if (!host) {
        error_handling("parse error~");
        exit(1);
    }
    printf("name is: %s\n", host->h_name); //官方域名
    for (i = 0; host->h_aliases[i]; i++) {
        printf("aliases %d: %s \n", i + 1, host->h_aliases[i]); //同一个IP可以绑定多个域名
    }
    printf("address type is: %s\n", (host->h_addrtype == AF_INET) ? "AF_INET" : "AF_INET6"); //IPV4|6
    for (i = 0; host->h_addr_list[i]; i++) {
        printf("IP addr %d : %s\n", i + 1, inet_ntoa(*(struct in_addr *) host->h_addr_list[i])); //域名对应的IP地址
    }
    printf("IP len: %d\n", host->h_length);//IP地址长度.4字节|16
    return 0;
}
