#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <unistd.h>

static int sid;

static void P() {
    //申请
    struct sembuf sbuf = {0, -1, 0};
    if (semop(sid, &sbuf, 1) < 0) {
        perror("semop");
        exit(1);
    }
}

static void V() {
    //释放
    struct sembuf sbuf = {0, 1, 0};
    if (semop(sid, &sbuf, 1) < 0) {
        perror("semop");
        exit(1);
    }
}

int main(int argc, char **argv) {
    const key_t key = ftok("/dev/null", 1);
    sid = semget(key, 1, IPC_CREAT | 0666);
    if (sid < 0) {
        perror("semget");
        exit(1);
    }
    union semun su;
    su.val = 0; // 初始值设为 0
    if (semctl(sid, 0,SETVAL, su) < 0) {
        perror("semctl");
        exit(1);
    }

    const pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        exit(1);
    }
    if (pid == 0) {
        puts("Child: waiting for parent process");
        P();
        printf("Child: received signal from parent\n");
        exit(0);
    }
    sleep(2);
    printf("Parent: signaling child\n");
    V();
    wait(NULL);
    semctl(sid, 0,IPC_RMID);
    return 0;
}
