#include <stdlib.h>
#include <stdio.h>
int main(int argc, char const *argv[])
{
   int *p;
   int **q;
   int a = 100, b = 200;
   p = &a;
   q = &p;
   printf("%d", **q);
   return 0;
}
