//
// Created by 田明博 on 2024/5/18.
// 生成一个随机数
//

static unsigned long next = 1;

int rand(){
    next = next * 1103515245 + 12345 ;
    return (unsigned int) ( next / 65536) % 32768;
}

void set_rand(unsigned int send){
    next = send;
}