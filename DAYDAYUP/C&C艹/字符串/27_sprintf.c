#include "stdio.h"

int main(){
    char *name="tian";
    int age=18;
    float weight=70.5;
    char format[60];
    sprintf(format, "name:%10s, age:%d, weight: %6.2f",name,age,weight); //格式化字符串，并保存到format中
    puts(format);

    return 0;
}
