//
// Created by 田明博 on 2024/6/22.
// 获取命令行参数

#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "string.h"
#include <unistd.h>

#define FMTSTRSIZE 1024

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage err...");
        exit(1);
    }
    char fmt[FMTSTRSIZE];
    char time_buf[100];
    fmt[0] = '\0';
    time_t t;
    struct tm *tm;
    int c;
    t = time(NULL);
    FILE *fp = stdout;
    tm = localtime(&t);
    while (1) {
        /**
         * HMSymd 支持的选项
         * : 参数的选项
         * - 识别非选项的传参
         * */
        c = getopt(argc, argv, "-H:MSy:md");
        if (c < 0)
            break;
        printf("%c daf", c);
        switch (c) {
            case 1:
                if (fp == stdout) {
                    fp = fopen(argv[optind - 1], "w");
                    if (fp == NULL) {
                        perror("Fopen()");
                        fp = stdout;
                    }
                }
                break;
            case 'H':
                if (strcmp(optarg, "12") == 0)
                    strncat(fmt, "%I(%P) ", FMTSTRSIZE);
                else if (strcmp(optarg, "24") == 0)
                    strncat(fmt, "%H ", FMTSTRSIZE);
                else
                    puts("invalid arg");
                break;
            case 'M':
                strncat(fmt, "%M ", FMTSTRSIZE);
                break;
            case 'S':
                strncat(fmt, "%S ", FMTSTRSIZE);
                break;
            case 'y':
                if (strcmp(optarg, "2") == 0)
                    strncat(fmt, "%y ", FMTSTRSIZE);
                else if (strcmp(optarg, "4") == 0)
                    strncat(fmt, "%Y ", FMTSTRSIZE);
                else
                    puts("invalid arg");
                break;
            case 'm':
                strncat(fmt, "%m ", FMTSTRSIZE);
                break;
            case 'd':
                strncat(fmt, "%d ", FMTSTRSIZE);
                break;
            default:
                break;
        }

    }
    strncat(fmt, "\n", FMTSTRSIZE);
    strftime(time_buf, 100, fmt, tm); //格式化时间
    fputs(time_buf, fp);
    if (fp != stdout)
        fclose(fp);
    return 0;
}
