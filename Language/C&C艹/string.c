#include <stdio.h>
#include <string.h>

int main(int argc, char const *argv[])
{
    char tmp[10] = "tian";
    char tmp2[10] = "ming", tmp3[12];
    int len;
    strcpy(tmp3, tmp2); //复制字符串
    len = strlen(tmp3);
    printf("%s\n", tmp3);
    printf("%d", len);
    printf("%d",strcmp(tmp2,tmp3));
    return 0;
}
