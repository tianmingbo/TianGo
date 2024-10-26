/**
pthread_rwlock_init()：初始化读写锁。
pthread_rwlock_rdlock()：获取读锁。
pthread_rwlock_wrlock()：获取写锁。
pthread_rwlock_unlock()：释放锁。
pthread_rwlock_destroy()：销毁读写锁。
*/

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

pthread_rwlock_t rwlock;
int share_source = 0;

void *reader(void *arg) {
    pthread_rwlock_rdlock(&rwlock);
    printf("share_source:%d\n", share_source);
    pthread_rwlock_unlock(&rwlock);
    pthread_exit(NULL);
}

void *writer(void *arg) {
    pthread_rwlock_wrlock(&rwlock);
    share_source++;
    pthread_rwlock_unlock(&rwlock);
    pthread_exit(NULL);
}


int main() {
    pthread_rwlock_init(&rwlock, NULL);
    pthread_t r1, r2, w1;
    int res;
    pthread_create(&r2, NULL, reader, NULL);
    res = pthread_create(&w1, NULL, writer, NULL);
    if (res) {
        puts("create w1 err");
        exit(1);
    }
    pthread_create(&r1, NULL, reader, NULL);
    pthread_join(r1, NULL);
    pthread_join(r2, NULL);
    pthread_join(w1, NULL);
    return 0;
}
