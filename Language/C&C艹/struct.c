#include <string.h>
#include <stdio.h>

struct Book
{
    char name[24];
    int price;
    char sdn[22];
    char author[33]; /* data */
};

void print(struct Book *book)
{
    printf("%s\n", book->author); //使用结构体的指针访问成员，使用->
    printf("%d", book->price);
};

int main(int argc, char const *argv[])
{

    struct Book book1;
    struct Book book2;
    book1.price = 20;
    strcpy(book1.author, "chendali");
    print(&book1); //结构体的地址

    {
        /* data */
    };

    return 0;
}
