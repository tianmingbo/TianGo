#include<stdio.h>

enum DAY
{
    MON=1, TUE, WED, THU, FRI, SAT, SUN
}day;

int main(int argc, char const *argv[])
{
    for(day=MON;day <= SUN;day++){
    printf("%d ",day);

    }
    return 0;
}
