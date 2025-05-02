#include <stdlib.h>
#include <stdio.h>
#include <sys/ipc.h>
#include<sys/types.h>
#include <sys/msg.h>
#include <unistd.h>
#include <string.h>

#include "common.h"


int main() {
    struct msg_st sbuf;

    const key_t key = ftok(KEYPATH,KEYPROJ);
    if (key < 0) {
        perror("ftok()");
        exit(1);
    }

    int msgid = msgget(key, IPC_CREAT | 0666);
    if (msgid < 0) {
        perror("msgget()");
        exit(1);
    }
    sbuf.mtype = 1;
    strcpy(sbuf.mtext.name, "Tian");
    sbuf.mtext.id = 100;
    sbuf.mtext.value = 100.0f;
    //消息体大小,不包括 long mtype
    if (msgsnd(msgid, &sbuf, sizeof(sbuf) - sizeof(long), 0) < 0) {
        perror("msgrcv()");
        exit(1);
    }

    puts("ok!");
    //销毁当前实例
    msgctl(key,IPC_RMID, 0);
    exit(0);
}
