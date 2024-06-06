//
// Created by 田明博 on 2024/5/31.
// 二进制IO
/**
 * size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream)
 * size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream)
 *      ptr：指向数据读取的存储位置的指针
 *      size：要读取的每个数据项的大小（以字节为单位）
 *      nmemb：要读取的数据项数量
 *      stream：指向 FILE 对象的指针，指定要读取数据的文件流
 * */
#include "apue.h"

struct Vehicle {
    float mileage;
    float price;
    char name[20];
};

int main() {
    FILE *fp = fopen("example.bin", "wb");
    if (!fp) {
        err_sys("open file err");
    }
    struct Vehicle bmw = {3.14, 2.56, "BMW"};
    struct Vehicle bm1;
    fwrite(&bmw, sizeof(struct Vehicle), 1, fp);
    fclose(fp);
    fp = fopen("example.bin", "rb");
    fread(&bm1, sizeof(struct Vehicle),1,fp);
    fclose(fp);
    printf("mileage: %f, price: %f, name: %s\n", bm1.mileage, bm1.price, bm1.name);
    return 0;
}