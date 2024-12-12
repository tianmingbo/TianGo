/**
 * 文件锁定,支持对文件中的任意字节数的区域加锁
 * fcntl()
 * lockf()
 * flock()
 * */

#include "fcntl.h"
#include "stdio.h"
#include "unistd.h"
#include "stdlib.h"

#define PROC_NUM 20
#define FNAME "/tmp/out"
#define BUFSIZE 1024

//加锁或解锁一个文件区域
int lock_reg(int fd, int cmd, int type, off_t offset, int whence, off_t len) {
    struct flock lock;
    lock.l_type = type;/* F_RDLCK, F_WRLCK, F_UNLCK */
    lock.l_start = offset;/* byte offset, relative to l_whence */
    lock.l_whence = whence;/* SEEK_SET, SEEK_CUR, SEEK_END */
    lock.l_len = len;/* #bytes (O means to EOF) */
    return (fcntl(fd, cmd, &lock));
}

static void handler() {
    FILE *fp = fopen(FNAME, "r+");
    char buf[BUFSIZE];

    if (fp == NULL) {
        perror("fopen()");
        exit(1);
    }
    int fd = fileno(fp);
    //进入临界区
    lockf(fd, F_LOCK, 0);

    fgets(buf, BUFSIZE, fp);
    fseek(fp, 0, SEEK_SET);
    sleep(1);
    fprintf(fp, "%d\n", atoi(buf) + 1);
    fflush(fp);

    //离开临界区
    lockf(fd, F_ULOCK, 0);

    fclose(fp);
}

int main() {
    pid_t pid;

    for (int i = 0; i < PROC_NUM; i++) {
        pid = fork();
        if (pid < 0) {
            perror("fork()");
            exit(1);
        }
        if (pid == 0) {
            handler();
            exit(0);
        }
    }

    for (int i = 0; i < PROC_NUM; i++) {
        wait(NULL);
    }

    return 0;
}