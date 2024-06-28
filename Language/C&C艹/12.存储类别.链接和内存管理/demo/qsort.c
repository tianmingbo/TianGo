/**
 * 排序整型值
 * void qsort(void *base, size_t nmemb, size_t size,  int (*compar)(const void *, const void *))
 * */

#include "stdlib.h"
#include "stdio.h"


int compare_int(const void *a, const void *b) {
    int i_a = *(int *) a;
    int i_b = *(int *) b;
    return i_a > i_b ? 1 : i_a < i_b ? -1 : 0;
}


int main() {
    int num, i;
    puts("inout num count:");
    if (scanf("%d", &num) != 1 || num < 0) {
        puts("illegal num");
        exit(1);
    }
    int *arr;
    arr = malloc(sizeof(int) * num);
    if (arr == NULL) {
        puts("malloc error");
        exit(1);
    }
    puts("input val:");
    for (i = 0; i < num; i++) {
        scanf("%d", arr + i);
    }
    qsort(arr, num, sizeof(int), compare_int);
    for (i = 0; i < num; i++) {
        printf("%d\n", arr[i]);
    }
    free(arr);
    return 0;
}