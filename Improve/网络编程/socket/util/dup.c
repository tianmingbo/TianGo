#include "unistd.h"
#include "stdio.h"

/**
 * 文件描述符复制
 * */

int main(int agrc, char *argv[]) {
    int cfd1, cfd2;
    char *str1 = "hello \n";
    char *str2 = "world \n";
    cfd1 = dup(1);//复制文件描述符
    cfd2 = dup2(cfd1, 7);//功能和dup类似,不过可以指定复制后的文件描述符
    printf("fd1= %d ,fd2= %d \n", cfd1, cfd2);
    write(cfd1, str1, sizeof(str1)); //输出,1是标准输出
    write(cfd2, str2, sizeof(str2));
    close(cfd1);
    close(cfd2);
    write(1, str1, sizeof(str1));
    close(1);
    write(1, str2, sizeof(str2));//把标准输出关了,所以不会输出
    return 0;
}