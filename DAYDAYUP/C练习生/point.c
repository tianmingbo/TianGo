// #include <stdio.h>

// int main ()
// {
//     int var_runoob = 10;
//     int *p;              // 定义指针变量
//     p = &var_runoob;

//    printf("var_runoob 变量的地址： %p\n", p); //输出地址
//    printf("var_runoob 变量的地址： %d", *p); //输出该地址的值
//    return 0;
// }

//指针的算术运算
// #include <stdio.h>
// #define MAX 3
// int main(int argc, char const *argv[])
// {
//     int p[] = {1, 22, 33};
//     int *ptr, i;
//     ptr = p; //也可以写作ptr==&p[0]
//     for (i = 0; i < MAX; i++)
//     {
//         printf("%d\n", i);
//         printf("%p->%d\n", ptr, *ptr);
//         ptr++; //++实际是指向了下一个元素，而不是+1
//     }

//     /* code */
//     return 0;
// }

//指针数组

// #include <stdio.h>
// int main(int argc, char const *argv[])
// {
//     int a[3] = {1, 2, 3};
//     int *ptr[3], i; //int类型的指针
//     for (i = 0; i < 3; i++)
//     {
//         ptr[i] = &a[i];
//         printf("ptr[%d]->%d\n", i, *ptr[i]);
//     }
//     return 0;
// }

//指向指针的指针
// #include <stdio.h>

// int main(int argc, char const *argv[])
// {
//     int v = 100;
//     int *ptr1 = &v;
//     int **ptr2 = &ptr1; //指向指针的指针，必须使用**
//     printf("v[%p]->%d\n", &v, v);
//     printf("ptr1[%p]->%d\n", ptr1, *ptr1);
//     printf("ptr2[%p]->%d\n", ptr2, **ptr2);
//     return 0;
// }

//传递指针给函数
// #include <stdio.h>
// double getSum(int *arr, int size);
// int main(int argc, char const *argv[])
// {
//     int a[] = {1, 2, 33, 44};
//     int res, size = 4;
//     res = getSum(a, size);
//     printf("%d", res);
//     return 0;
// }
// double getSum(int *arr, int size) //接收数组作为参数
// {
//     int i, sum;
//     for (i = 0; i < size; i++)
//     {
//         sum += arr[i];
//     }
//     return sum;
// }

//函数指针

#include <stdio.h>
int max(int x, int y)
{
    return x > y ? x : y;
}

int main(int argc, char const *argv[])
{
    int (*p)(int, int) = max; //指向函数的指针
    printf("%d", p(1, 2));
    return 0;
}


//指向指針的指針
// #include <stdlib.h>
// #include <stdio.h>
// int main(int argc, char const *argv[])
// {
//    int *p;
//    int **q;
//    int a = 100, b = 200;
//    p = &a;
//    q = &p;
//    printf("%d", **q);
//    return 0;
// }
