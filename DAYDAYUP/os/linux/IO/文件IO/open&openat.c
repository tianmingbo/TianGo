//
// Created by 田明博 on 2024/5/27.
//
/**
 * #include <fcntl.h>
 * int open(const char *pathname, int flags, mode_t mode);
 *      pathname: 是要打开的文件的路径名。
 *      flags: 是打开文件时的标志，如只读、只写、追加等。
 *      mode: 是新建文件时的权限。
 * #include <fcntl.h>
 * int openat(int dirfd, const char *pathname, int flags, mode_t mode);
 *      dirfd 是已打开目录的文件描述符,如果为 AT_FDCWD，则相对于当前工作目录打开文件。
 *
 * 常见的 flags 包括：
        O_RDONLY: 只读方式打开文件。
        O_WRONLY: 只写方式打开文件。
        O_RDWR: 读写方式打开文件。
        O_CREAT: 如果文件不存在则创建文件。
        O_TRUNC: 如果文件存在且是普通文件，则将其长度截断为0。
        O_APPEND: 在文件末尾追加数据而不覆盖已有数据。
        O_EXCL: 与 O_CREAT 一同使用，确保文件不存在，防止竞态条件。
        O_NONBLOCK 或 O_NDELAY: 非阻塞模式打开文件。
        O_SYNC: 同步写入，确保数据写入磁盘后 write 系统调用返回。
        O_DIRECTORY: 仅打开目录。
 * */

#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    int fd;
    char buffer[1024];

    // 打开一个文件，如果不存在则创建，以读写方式打开，追加数据到文件末尾
    fd = open("example.txt", O_CREAT | O_RDWR | O_APPEND, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    // 写入数据到文件
    if (write(fd, "Hello, Tian!\n", 14) != 14) {
        perror("write");
        close(fd);
        return 1;
    }

    // 将文件指针移到文件开头
    if (lseek(fd, 0, SEEK_SET) == -1) {
        perror("lseek");
        close(fd);
        return 1;
    }

    // 读取文件内容并输出到标准输出, read()返回读到的字节数,若已到文件尾,返回0.若出错,返回-1
    ssize_t bytes_read;
    while ((bytes_read = read(fd, buffer, sizeof(buffer))) > 0) {
        //write() 若成功,返回已写的字节数;出错返回-1
        if (write(STDOUT_FILENO, buffer, bytes_read) != bytes_read) {
            perror("write");
            close(fd);
            return 1;
        }
    }

    // 关闭文件,成功返回0,失败返回-1
    if (close(fd) == -1) {
        perror("close");
        return 1;
    }

    return 0;
}