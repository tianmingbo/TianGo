//
// Created by 田明博 on 2024/6/17.
// 递归遍历文件类型
#include "stdio.h"
#include "stdlib.h"
#include "sys/stat.h"
#include "apue.h"
#include <dirent.h>

typedef int Myfunc(const char *pathname, const struct stat *stat_ptr, int type);

static Myfunc myfunc;

static int do_path(Myfunc *func);

static int myftw(char *pathname, Myfunc *func);

static long nreg, ndir, nblk, nchr, nfifo, nslink, nsock, ntot;

int main(int argc, char **argv) {
    if (argc < 2) {
        puts("Usage...");
        exit(1);
    }
    int ret = myftw(argv[1], myfunc);
    ntot = nreg + ndir + nblk + nchr + nfifo + nslink + nsock;
    printf("total: %7ld\n", ntot);
    printf("普通文件:%7ld\n", nreg);
    printf("目录文件:%7ld\n", ndir);
    printf("块特殊文件:%7ld\n", nblk);
    printf("字符特殊文件:%7ld\n", nchr);
    printf("管道:%7ld\n", nfifo);
    printf("符号链接:%7ld\n", nslink);
    return ret;
}

#define  FTW_F 1 //not dir
#define FTW_D 2 //dir
#define FTW_DNR 3 //dir读失败
#define FTW_NS 4 //stat失败
#define MAX_PATH_LEN 1024

static char *fullpath;

static int myftw(char *pathname, Myfunc *func) {
    if ((fullpath = malloc(MAX_PATH_LEN)) == NULL) {
        perror("malloc()");
        exit(1);
    }

    strcpy(fullpath, pathname);
    return do_path(func);
}

static int do_path(Myfunc *func) {
    struct stat file_info;
    int ret, n;
    DIR *dp;
    struct dirent *dirp;
    if (lstat(fullpath, &file_info) < 0) //获取文件属性
        return func(fullpath, &file_info, FTW_NS);
    if (S_ISDIR(file_info.st_mode) == 0) //普通文件,直接计数
        return func(fullpath, &file_info, FTW_F);
    func(fullpath, &file_info, FTW_D); //文件夹计数一次
    n = strlen(fullpath);
    fullpath[n++] = '/';
    fullpath[n] = 0;
    if ((dp = opendir(fullpath)) == NULL) {
        perror("opendir()");
        exit(1);
    }
    while ((dirp = readdir(dp)) != NULL) {
        if (strcmp(dirp->d_name, ".") == 0 || strcmp(dirp->d_name, "..") == 0)
            continue;
        strcpy(&fullpath[n], dirp->d_name); //拼接内部的文件夹名
        if ((ret = do_path(func)) != 0) //递归
            break;
    }
    fullpath[n - 1] = 0; //状态恢复
    closedir(dp);
    return ret;

}

static int myfunc(const char *pathname, const struct stat *stat_ptr, int type) {
    switch (type) {
        case FTW_F:
            switch (stat_ptr->st_mode & S_IFMT) {
                case S_IFREG:
                    nreg++;
                    break;
                case S_IFBLK:
                    nblk++;
                    break;
                case S_IFCHR:
                    nchr++;
                    break;
                case S_IFIFO:
                    nfifo++;
                    break;
                case S_IFLNK:
                    nslink++;
                    break;
                case S_IFSOCK:
                    nsock++;
                    break;
                case S_IFDIR:
                    fprintf(stderr, "%s it is a dir\n,", pathname);
            }
            break;
        case FTW_D:
            ndir++;
            break;
        case FTW_DNR:
            fprintf(stderr, "can't read dir %s\n", pathname);
            break;
        case FTW_NS:
            fprintf(stderr, "stat err %s\n", pathname);
            break;
        default:
            fprintf(stderr, "UNK %s\n", pathname);
    }
    return 0;
}