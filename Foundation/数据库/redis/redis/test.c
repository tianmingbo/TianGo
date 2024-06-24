#include <stdio.h>


int main(void) {
    short test[4][2] = {{2, 4},
                        {6, 8},
                        {1, 3},
                        {5, 7}};
    printf("test= %p, test+1= %p\n", test, test + 1);
    printf("test= %p, test+1 =%p\n", test, test + 1); //和上一条等价

    printf("test[0]= %p, test[0]+1= %p\n", test[0], test[0] + 1);
    printf("*test=   %p, *test +1 = %p\n", *test, *test + 1);//和上一条等价

    printf("%d,%d,%d\n", test[0][0], *test[0], **test); //等价
    printf("%d,%d\n", test[2][1], *(*(test + 2) + 1));//等价
    return 0;
}