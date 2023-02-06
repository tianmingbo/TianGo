#include <stdio.h>
#include <string.h>
 
int main ()
{
   const char src[50] = "http://www.runoob.com";
   char dest[99]="tian";
 
   memcpy(&dest[0]+strlen(dest), src, strlen(src)+1);
   printf("dest = %s\n", dest);
   
   return(0);
}