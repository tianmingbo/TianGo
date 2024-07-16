//
// Created by 田明博 on 2024/7/11.
//
/**
 * sigaction
 * */

#include <stdio.h>
#include <stdlib.h>
#include <sys/syslog.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>

#define FNAME "/tmp/out"
static FILE *fp;

static void daemon_exit(int s) {
    closelog();
    fprintf(fp, "%s\n", "end");
    fflush(NULL);
    fclose(fp);
    exit(0);
}

static int deamonize() {
    int fd;
    pid_t pid;
    pid = fork();

    if (pid < 0) {
        return -1;
    }

    if (pid > 0) {
        exit(0);
    }

    fd = open("/dev/null", O_RDWR);//输出都忽略
    if (fd < 0) {
        return -1;
    }
    if (pid == 0) {
        printf("test\n");
        fflush(NULL);
        dup2(fd, 0);
        dup2(fd, 1);
        dup2(fd, 2);
        if (fd > 2) {
            close(fd);
        }
        setsid();//脱离终端
        //umask();
        chdir("/");
    }
    return 0;
}

int main() {

    //开启日志服务
    openlog("print i", LOG_PID, LOG_DAEMON);

    if (deamonize()) {
        syslog(LOG_ERR, "init failed!");
    } else {
        syslog(LOG_INFO, "successded!");
    }
    struct sigaction sa;
    sa.sa_handler = daemon_exit; //信号处理函数
    sigemptyset(&sa.sa_mask);
    sigaddset(&sa.sa_mask, SIGTERM);
    sigaddset(&sa.sa_mask, SIGQUIT);
    sigaddset(&sa.sa_mask, SIGINT);
    sa.sa_flags = 0;
    sigaction(SIGTERM, &sa, NULL); //在响应SIGTERM信号时,停止响应SIGTERM/SIGQUIT/SIGINT
    sigaction(SIGQUIT, &sa, NULL);
    sigaction(SIGINT, &sa, NULL);

    fp = fopen(FNAME, "w+");
    if (fp == NULL) {
        syslog(LOG_ERR, "write file failed!");
        exit(1);
    }

    syslog(LOG_INFO, "%s opened", FNAME);

    for (int i = 0;; i++) {
        fprintf(fp, "%d\n", i);
        fflush(NULL);
        syslog(LOG_DEBUG, "%d 写入", i);
        sleep(1);
    }


}
