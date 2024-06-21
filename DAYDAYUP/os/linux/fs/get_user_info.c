//
// Created by 田明博 on 2024/6/19.
// 根据name获取/etc/passwd里的值

#include "stdio.h"
#include <pwd.h>
#include "string.h"

struct passwd *get_passwd_info(const char *);

int main() {
    char *name = "root";
    struct passwd *res = get_passwd_info(name);
    printf("%s\n", res->pw_name);
    printf("%d\n", res->pw_uid);
    return 0;
}

struct passwd *get_passwd_info(const char *name) {
    struct passwd *ptr;
    setpwent();//依次遍历passwd
    while ((ptr = getpwent()) != NULL)
        if (strcmp(name, ptr->pw_name) == 0)
            break;
    endpwent();
    return ptr;
}
