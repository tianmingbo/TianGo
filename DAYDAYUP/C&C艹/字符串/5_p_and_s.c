//
// Created by 田明博 on 2024/5/15.
// 指针和字符串
//

#include "stdio.h"

int main() {
    char *msg = "tian is a good man";
    char *copy;
    copy = msg;
    printf("msg  = \"%s\", &msg=  %p, msg-> %p\n", msg, &msg, msg);
    printf("copy = \"%s\", &copy= %p, copy->%p\n", copy, &copy, copy);
    /*
     * 并未copy字符串,仅仅是指向该地址
     * msg  = "tian is a good man", &msg=  0x7ff7b4b38750, msg-> 0x10b3caf54
     * copy = "tian is a good man", &copy= 0x7ff7b4b38748, copy->0x10b3caf54
     * */
    return 0;
}