//
// 把文件内容压缩为原来的1/3
//

#include "stdlib.h"
#include "stdio.h"
#include "string.h"

#define LEN 40

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage:%s filename\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    FILE *in, *out;
    if ((in = fopen(argv[1], "r")) == NULL) {
        fprintf(stderr, "Couldn't open the file:%s\n", argv[1]);
        exit(EXIT_FAILURE);
    }
    //设置输出文件名
    char name[LEN];
    strncpy(name, argv[1], LEN - 5);
    name[LEN - 5] = '\0';
    strcat(name, ".red");
    if ((out = fopen(name, "w")) == NULL) {
        fprintf(stderr, "Can't create file!\n");
        exit(3);
    }
    int ch, count = 0;
    //拷贝数据
    while ((ch = getc(in)) != EOF)
        if (count++ % 3 == 0)
            putc(ch, out);
    //收尾
    if (fclose(in) != 0 || fclose(out) != 0)
        fprintf(stderr, "Error in closing files\n");
    return 0;
}
