//
// 使用fprintf()/fscanf()/rewind()
//

#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define LEN 41

/**
 * fprintf()/fscanf()类似printf、scanf。只不过第一位是文件描述符。
 * rewind把指针指向文件开始位置
 * */
int main() {
    FILE *fp;
    char words[LEN];
    if ((fp = fopen("words", "a+")) == NULL) {
        fprintf(stderr, "Couldn't open the \"words\" file \n");
        exit(EXIT_FAILURE);
    }
    puts("Enter words to add to the file；press the # exit");
    while ((fscanf(stdin, "%40s", words) == 1) && (words[0] != '#'))
        fprintf(fp, "%s\n", words);
    puts("File Contents:");
    rewind(fp); //返回到文件开始处
    while (fscanf(fp, "%s", words) == 1)
        puts(words);
    puts("Done");
    if (fclose(fp) != 0)
        fprintf(stderr, "Error closing file\n");
    return 0;
}
