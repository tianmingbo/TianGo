/**
 * 每个字段占用特定的位数
 * */
#include <stdio.h>

// 定义一个结构体，包含位段
struct {
    unsigned int flag1: 1;   // 占用1位的无符号整数
    unsigned int flag2: 2;   // 占用2位的无符号整数
    unsigned int flag3: 3;   // 占用3位的无符号整数
} status;

int main() {
    status.flag1 = 1;  // 设置 flag1 为 1
    status.flag2 = 3;  // 设置 flag2 为 3
    status.flag3 = 7;  // 设置 flag3 为 7

    // 打印每个位段的值
    printf("flag1: %u\n", status.flag1);
    printf("flag2: %u\n", status.flag2);
    printf("flag3: %u\n", status.flag3);

    // 打印整个结构体的大小
    printf("Size of status: %zu bytes\n", sizeof(status));

    return 0;
}
