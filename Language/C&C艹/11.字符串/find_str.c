/**
 * char *strchr(const char *s, int c); 返回一个指向该位置的指针，第一个
 * char *strrchr(const char *s, int c); 返回一个指向该位置的指针，最后一个
 * char  *strpbrk( char const *str, char const *grouip); 查找任何一组字符第1次在字符串中出现的位置
 * char *strstr( char const *s1, char ceonst *s2); 在字符串中查找一个子串。如果没找到，返回NULL，如果子串为空，返回s1
 * size_t strspn(char const *str, char conist *group ); 返回str起始部分匹配group中任意字符的字符数
 * size_t strcspn(char cosnt *str, char coonst *group );
 * char *strtok( char *str, char const *sep ); str="hello world !!" seq=" "，则计算过程为"hello\0" "world\0" "!!0"
 * */
#include "stdio.h"
#include "string.h"

int main() {
    char strings[] = "hello world !!";
    char *res;
    res = strchr(strings, 'l');
    printf("%s\n", res);

    //****************************************
    res = strpbrk(strings, "aeiou");//e第一次出现index=1
    printf("%s\n", res);
    //****************************************
    res = strstr(strings, "ld");
    printf("%s\n", res);
    //****************************************
    size_t len = strspn(strings, "leh,"); //匹配hell
    printf("%zu\n", len);
    //****************************************
    res = strtok(strings, " ");
    while (res != NULL) {
        puts(res);
        res = strtok(NULL, " ");
    }
    return 0;
}