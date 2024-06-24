#include <unistd.h>
#include <malloc/_malloc.h>
#include <string.h>
#include "stdio.h"
#include "pthread.h"

void *thread_main(void *arg);

int main(int argc, char *argv[]) {
    pthread_t t_id;
    int thread_params = 5;
    void *thr_status;
    if (pthread_create(&t_id, NULL, thread_main, (void *) &thread_params) != 0) {
        puts("pthread_create() error");
        return -1;
    }
    //等待参数为id的线程结束
    if (pthread_join(t_id, &thr_status) != 0) {
        puts("pthread_join() error");
        return -1;
    }
    printf("Thread return msg: %s\n", (char *) thr_status);
    free(thr_status);
    return 0;
}

void *thread_main(void *arg) {
    int i;
    int cnt = *((int *) arg);
    char *msg = (char *) malloc(sizeof(char) * 50);
    strcpy(msg, "Hello, I am thread \n ");
    for (i = 0; i < cnt; i++) {
        sleep(1);
        puts("running thread");
    }
    return (void *) msg;
}
