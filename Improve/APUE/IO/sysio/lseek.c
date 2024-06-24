//
// Created by 田明博 on 2024/5/27.
//
/**
 * lseek() 函数有三个参数：
    int fd：文件描述符，指定了要进行操作的文件。
    off_t offset：偏移量，指定了要移动的距离。正值表示向文件尾部移动，负值表示向文件起始位置移动。
    int whence：参考点，指定了偏移量的参考位置。可以取三个值：
        SEEK_SET：从文件起始位置开始计算偏移量。
        SEEK_CUR：从当前文件指针位置开始计算偏移量。
        SEEK_END：从文件末尾位置开始计算偏移量。
 * */
#include "apue.h"
#include "fcntl.h"

char buf1[] = "abcdefghi";
char buf2[] = "ABCDEFGHI";

int main() {
    int fd;
    if ((fd = creat("file.hole", FILE_MODE)) < 0)
        err_sys("create_error");
    if (write(fd, buf1, 10) != 10) //offset=10
        err_sys("buf1 write error");
    if (lseek(fd, 16384, SEEK_SET) == -1) //offset=16384
        err_sys("lseek error");
    if (write(fd, buf2, 10) != 10)//offset=16394
        err_sys("buf2 write error");
    return 0;
}

