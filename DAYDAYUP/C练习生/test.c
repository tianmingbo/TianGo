#include<stdio.h>
void swap(int *x,int *y);
int main(int argc, char const *argv[])
{
   int x=100;
   int y=200;
   swap(&x,&y);
   printf("%d,%d", x , y);
   return 0;
}
void swap(int *x ,int *y){
   int tmp;
   tmp = *x;
   *x = *y;
   *x = tmp;
}