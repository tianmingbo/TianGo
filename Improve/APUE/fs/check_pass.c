//
// Created by 田明博 on 2024/6/21.
// 密码校验

#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "shadow.h"
#include "string.h"
#include <crypt.h>

int main(int argc, char **argv) {
    if (argc < 2) {
        puts("Usage ..");
        exit(1);
    }
    char *passwd = getpass("input passwd");
    struct spwd *shadow_line = getspnam(passwd);
    printf("%s\n", shadow_line->sp_pwdp);
    char *encrypted = crypt(passwd, shadow_line->sp_pwdp);
    if (strcmp(shadow_line->sp_pwdp, encrypted) == 0)
        puts("OK");
    else
        puts("failed");
    return 0;
}
