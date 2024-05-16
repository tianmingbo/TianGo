#include "stdio.h"
#include "string.h"

int main(){
    char msg[]="abcdefghijklmnopqrstuvwxyz";
    char dest[20];
    strncpy(dest,msg,5);
    dest[5]='\0'; //strncpy并不保证字符串以\0结尾，所以需要手动添加
    puts(dest);
    return 0;
}
