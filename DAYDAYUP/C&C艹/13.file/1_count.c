//
// Created by 田明博 on 2024/5/18.
//
#include "stdlib.h"
#include "stdio.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage : %s filename\n ", argv[0]);
        exit(EXIT_FAILURE);
    }
    FILE *fp;
    if ((fp = fopen(argv[1], "r")) == NULL) {
        printf ( "Can' t open %s\n" , argv [ l ] ) ;
        exit ( EXIT FAILURE ) ;
    }
}