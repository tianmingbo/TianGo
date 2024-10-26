/**
 * 互斥量
 * */

#include "stdlib.h"
#include "string.h"
#include "stdio.h"
#include "pthread.h"

#define TNUM 20
#define FNAME "/tmp/out"
//静态分配的互斥量
static pthread_mutex_t mux = PTHREAD_MUTEX_INITIALIZER;

static void *func(void *arg) {
    FILE *fp;
    char buf[1024];
    pthread_mutex_lock(&mux);
    fp = fopen(FNAME, "r+");
    fgets(buf, 1024, fp);
    fseek(fp, 0, SEEK_SET);
    puts(buf);
    fprintf(fp, "%d\n", atoi(buf) + 1);
    fclose(fp);
    pthread_mutex_unlock(&mux);
    pthread_exit(NULL);
}

int main() {
    int err, i;
    pthread_t tid[TNUM];
    for (i = 0; i < TNUM; i++) {
        err = pthread_create(tid + i, NULL, func, NULL);
        if (err) {
            fprintf(stderr, "%s", strerror(err));
            exit(1);
        }
    }
    for (i = 0; i < TNUM; i++) {
        pthread_join(tid[i], NULL);
    }
    pthread_mutex_destroy(&mux);
    return 0;
}