#include <stdlib.h>
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/types.h>
#include <sys/msg.h>
#include <unistd.h>

#include "common.h"


int main() {
    struct msg_st rbuf;

    const key_t key = ftok(KEYPATH,KEYPROJ);
    if (key < 0) {
        perror("ft0k()");
        exit(1);
    }

    int msgid = msgget(key, 0);
    if (msgid < 0) {
        perror("msgget()");
        exit(1);
    }

    while (1) {
        if (msgrcv(msgid, &rbuf, sizeof(rbuf) - sizeof(long), 0, 0) < 0) {
            perror("msgrcv()");
            exit(1);
        }
        printf("name: %s ", rbuf.mtext.name);
        printf("id: %d ", rbuf.mtext.id);
        printf("value: %.2f\n", rbuf.mtext.value);
        fflush(stdout);
    }
    //销毁当前实例
    msgctl(key,IPC_RMID, 0);

    exit(0);
}
