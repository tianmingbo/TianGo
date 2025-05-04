#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <string.h>

#define BUFSIZE 1024

int main() {
    const key_t key = ftok("/dev/null", 1);
    const int shmid = shmget(key, BUFSIZE, IPC_CREAT | 0666);
    char *data;
    if (shmid < 0) {
        perror("shmget");
        exit(1);
    }
    const pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        exit(1);
    }
    if (pid == 0) {
        sleep(2);
        puts("Child: waiting for parent process");
        data = shmat(shmid, NULL, 0);
        puts(data);
        shmdt(data);
        exit(0);
    }
    data = shmat(shmid, NULL, 0);
    strcpy(data, "Hello World");
    shmdt(data);
    wait(NULL);
    shmctl(shmid, IPC_RMID, NULL);
    return 0;
}
