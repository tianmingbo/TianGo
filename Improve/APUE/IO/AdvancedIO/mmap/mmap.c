/**
 * 存储映射IO,一种将文件或其他设备映射到进程的虚拟地址空间中的技术.
 * 进程可以直接读写内存来操作文件或设备，而无需使用传统的 read 和 write 系统调用。
 * */
// find 'a'

#include "stdlib.h"
#include "fcntl.h"
#include "stdio.h"
#include <sys/stat.h>
#include <sys/mman.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        puts("Usage err");
        exit(1);
    }
    int i, count = 0;
    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) {
        perror("open()");
        exit(1);
    }
    struct stat f_stat;
    int res = fstat(fd, &f_stat);
    if (res < 0) {
        perror("fstat()");
        exit(1);
    }
    char *mapped_mem = mmap(NULL, f_stat.st_size, PROT_READ, MAP_SHARED, fd, 0);
    if (mapped_mem == MAP_FAILED) {
        perror("mmap()");
        exit(1);
    }
    close(fd); //文件关闭,并不会影响映射

    for (i = 0; i < f_stat.st_size; i++) {
        if (mapped_mem[i] == 'a') {
            count++;
        }
    }
    printf("%d\n", count);
    munmap(mapped_mem, f_stat.st_size); //解除映射
    exit(0);
}