//
// Created by 田明博 on 2024/6/21.
//
#include "time.h"
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"

#define FNAME "/tmp/out"
#define BUFSIZE 1024

int main() {
    int count = 0;
    FILE *fp = fopen(FNAME, "a+");
    struct tm *tm;
    char buf[BUFSIZE];
    time_t t;
    if (fp == NULL) {
        perror("fopen()");
        exit(1);
    }
    while (fgets(buf, BUFSIZE, fp) != NULL) {
        count++;
    }

    while (1) {
        time(&t);
        tm = localtime(&t);
        fprintf(fp, "%-4d%d-%d-%d %d:%d:%d\n", ++count, 1900 + tm->tm_year, tm->tm_mon + 1,
                tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);
        fflush(fp);
        sleep(1); //unistd.h
    }
    fclose(fp);
    return 0;
}