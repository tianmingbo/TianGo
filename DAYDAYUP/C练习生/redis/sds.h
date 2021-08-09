#include <stdio.h>
#include<stdlib.h>
#include <string.h>


typedef char *sds;
struct sdshdr
{
    int len;    //已占用的长度
    int free;   //未使用的长度
    char buf[]; //数据空间
};

