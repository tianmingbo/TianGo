/**
 * 内存操作
 * void *memcpy(void *dst, void const *src, size_t length); 将源内存区域的内容复制到目标内存区域中，不考虑这两个区域是否重叠。
 * void *memmove(void *dst, void const *src, size_t length); 将源内存区域 src 的内容复制到目标内存区域 dest 中，共复制 n 个字节
 * void *memcmp( void const *a, void const *b, size_t length); 对两段内存的内容进行比较，共比较length个
 * void *memchr(void const *a, int ch, size_t length); 从a的起始位置开始查找字符ch第一次出现的位置，返回一个指向该位置的指针，查找lenght个字节
 * void *memset(void *a, int ch, size_t length); 把从a开始的length个字节都设置为ch
 * */
#include <stdio.h>
#include <string.h>

int main() {
    char str1[20] = "tianm";
    char str2[] = "Hello, world!";

    // 将 str2 的内容复制到 str1 的位置
//    memcpy(str1, str2, strlen(str2) + 1); // 复制整个字符串，包括结尾的空字符 '\0'
//    puts(str1);
    memmove(str1, str2, 4);  // 移动前4个字符
    puts(str1);
    puts("******************************************");
    int arr[5] = {1, 2, 3, 4, 5};
    int search_value = 3;
    size_t size = sizeof(arr);

    // 使用 memchr 查找整数 3 在数组 arr 中的位置
    int *result = (int *) memchr(arr, search_value, size);
    printf("%lld\n", result - arr);
    puts("******************************************");
    memset(arr, 0, size);
    for (int i = 0; i < 5; i++) {
        printf("%d\n", arr[i]);
    }
    return 0;

}
