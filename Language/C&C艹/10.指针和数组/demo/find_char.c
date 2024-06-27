/**
 * 在字符串数组中查找字符
 * */

#include "stdio.h"
#include "assert.h"

#define TRUE 1
#define FALSE 0

int find_char(char **strings, int value) {
    assert(strings != NULL);
    //遍历行
    while (*strings != NULL) {
        //遍历每个字符
        while (*(*strings) != '\0') {
            if (*(*strings)++ == value)
                return TRUE;
        }
        strings++;
    }
    return FALSE;
}

int main() {
    char *str[] = {"tian", "ming", "da", "6"};
    int res = find_char(str, 't');
    printf("%d\n", res);
    return 0;
}