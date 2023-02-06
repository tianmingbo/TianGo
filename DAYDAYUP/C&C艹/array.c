// #include<stdio.h>

// int main(int argc, char const *argv[])
// {
//     int a[10];
//     int i,j;
//     for(i=0;i<10;i++){
//         a[i]=100;
//     }
//     for (j=0;j<10;j++){
//         printf("%d", a[j]);
//     }
//     return 0;
// }


//*******************多维数组
// #include<stdio.h>
// int main(int argc, char const *argv[])
// {
//     int a[3][4]={{1,2,3,4},{5,6,7,8},{9,10,11,12}};
//     int i,j;
//     for (i=0;i<3;i++){
//         for(j=0;j<4;j++){
//             printf("%d ",a[i][j]);
//         }
//     }
//     return 0;
// }




//数组作为参数传递
// #include <stdio.h>
 
// /* 函数声明 */
// double getAverage(int arr[], int size);
 
// int main ()
// {
//    /* 带有 5 个元素的整型数组 */
//    int balance[5] = {1000, 2, 3, 17, 50};
//    double avg;
 
//    /* 传递一个指向数组的指针作为参数 */
//    avg = getAverage( balance, 5 ) ;
 
//    /* 输出返回值 */
//    printf( "平均值是： %f ", avg );
    
//    return 0;
// }
 
// double getAverage(int *arr, int size)
// {
//   int    i;
//   double avg;
//   double sum=0;
 
//   for (i = 0; i < size; i++)
//   {
//     printf("%d ",i);
//     sum += arr[i];
//   }
 
//   avg = sum / size;
 
//   return avg;
// }





//**********函数返回数组
/* 要生成和返回随机数的函数 */
// #include<stdio.h>
// #include<stdlib.h>
// #include<time.h>

// int * getRandom( )
// {
//   static int  r[10];
//   int i;
 
//   /* 设置种子 */
//   srand( (unsigned)time( NULL ) );
//   for ( i = 0; i < 10; ++i)
//   {
//      r[i] = rand();
//      printf( "r[%d] = %d\n", i, r[i]);
 
//   }
 
//   return r;
// }
 
// /* 要调用上面定义函数的主函数 */
// int main ()
// {
//    /* 一个指向整数的指针 */
//    int *p;
//    int i;
 
//    p = getRandom();
//    for ( i = 0; i < 10; i++ )
//    {
//        printf( "*(p + %d) : %d\n", i, *(p + i));
//    }
 
//    return 0;
// }




//指向数组的指针
#include<stdlib.h>
#include<stdio.h>

int main(int argc, char const *argv[])
{
    double balance[10]={1.0,2,3,4,5};
    double *p;
    p=balance;
    printf("%f",*p);
    printf("%f",*(p+1));
    //数组名是指向数组中一个元素的常量指针，balance是指向&balance[0]的指针
    return 0;
}
