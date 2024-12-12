/**
 * 父子进程通信
 * */

#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define MEMSIZE 1024

int main() {
    //匿名映射可以实现malloc的功能
    char *mem_map = mmap(NULL, MEMSIZE, PROT_WRITE | PROT_READ, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (mem_map == MAP_FAILED) {
        perror("mmap()");
        exit(1);
    }
    int pid = fork();
    if (pid < 0) {
        perror("fork()");
        munmap(mem_map, MEMSIZE);
        exit(1);
    } else if (pid == 0) {
        strcpy(mem_map, "hello"); //child write
        munmap(mem_map, MEMSIZE);
        exit(0);
    } else {
        wait(NULL);
        puts(mem_map); //parent read
        munmap(mem_map, MEMSIZE);
        exit(0);
    }
}