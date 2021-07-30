#include <stdio.h>
#ifndef MESSAGE
#define MESSAGE "You wish!"
#endif
int main(int argc, char const *argv[])
{
   printf("%s\n", MESSAGE);
   printf("%s", __DATE__);
   return 0;
}
