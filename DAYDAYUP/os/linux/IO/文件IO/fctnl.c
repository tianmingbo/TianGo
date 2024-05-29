//
// Created by 田明博 on 2024/5/28.
//

#include <fcntl.h>

int fcntl(int fd, int cmd, ... /* arg */ );
/**
 * fd是文件描述符
 * cmd是要执行的操作,arg取决于cmd的值
 *  F_DUPFD：复制文件描述符。
 *  F_GETFD：获取文件描述符标志。
 *  F_SETFD：设置文件描述符标志。
 *  F_GETFL：获取文件状态标志和访问模式。
 *  F_SETFL：设置文件状态标志和访问模式。
 *  F_GETOWN,F_SETOWN: 获取/设置异步IO所有权.
 *  F_GETLK、F_SETLK、F_SETLKW：获取或设置文件锁。
 * */
#include "apue.h"

int main() {
    int fd = open("example.txt", O_RDONLY); // 打开文件 example.txt

    if (fd == -1) {
        perror("Failed to open file");
        exit(EXIT_FAILURE);
    }

    // 获取文件描述符的标志信息
    int flags = fcntl(fd, F_GETFL, 0);

    if (flags == -1) {
        perror("Failed to get flags");
        exit(EXIT_FAILURE);
    }

    // 输出文件描述符的标志信息
    printf("File descriptor %d flags before change: %d\n", fd, flags);

    // 设置新的标志信息（在原有标志的基础上添加非阻塞模式）
    flags |= O_NONBLOCK;

    // 将新的标志信息应用到文件描述符上
    if (fcntl(fd, F_SETFL, flags) == -1) {
        perror("Failed to set flags");
        exit(EXIT_FAILURE);
    }

    // 获取并输出更改后的文件描述符的标志信息
    flags = fcntl(fd, F_GETFL, 0);
    printf("File descriptor %d flags after change: %d\n", fd, flags);

    // 关闭文件描述符
    close(fd);

    return 0;
}