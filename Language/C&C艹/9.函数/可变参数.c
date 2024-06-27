/**
 * 参数不定
 * */

#include <stdio.h>
#include <stdarg.h>

// 计算一组数字的平均值
double average(int count, ...) {
    va_list args;               // 定义一个 va_list 类型的变量
    va_start(args, count);      // 初始化 args，使其指向第一个可选参数

    double sum = 0;
    for (int i = 0; i < count; i++) {
        sum += va_arg(args, double);  // 访问列表中的每个参数
    }

    va_end(args);               // 处理完参数列表后清理 va_list

    return sum / count;
}

int main() {
    double avg1 = average(3, 2.0, 3.5, 6.5);
    double avg2 = average(5, 1.0, 2.0, 3.0, 4.0, 5.0);

    printf("平均值 1: %.2f\n", avg1);
    printf("平均值 2: %.2f\n", avg2);

    return 0;
}