#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include "errno.h"
#include "mytbf.h"
#include <sys/time.h>

struct mytbf_st {
    int csp;
    int burst;
    int token;
    int pos;//任务列表的下标
};

static struct mytbf_st *job[MYTBF_MAX];
static volatile int inited = 0;

static void (*alarm_status)(int);

static struct sigaction oldact;

static int get_free_pos() {
    for (int i = 0; i < MYTBF_MAX; i++) {
        if (job[i] == NULL)
            return i;
    }
    return -1;
}


//信号处理函数
static void handler(int sig, siginfo_t *st, void *context) {
    if (st->si_code == SI_USER)
        return;
    for (int i = 0; i < MYTBF_MAX; i++) {
        if (job[i] != NULL) {
            job[i]->token += job[i]->csp;
            if (job[i]->token > job[i]->burst) {
                job[i]->token = job[i]->burst;
            }
        }
    }
}

//装载信号处理模块
static void mod_load() {
    struct sigaction act;
    act.sa_flags = SA_SIGINFO;
    act.sa_sigaction = handler;
    sigaction(SIGALRM, &act, &oldact);
    struct itimerval timer;

    timer.it_interval.tv_sec = 1;
    timer.it_interval.tv_usec = 0;

    timer.it_value.tv_sec = 1;
    timer.it_value.tv_usec = 0;
    // 启动定时器
    if (setitimer(ITIMER_REAL, &timer, NULL) == -1) {
        perror("setitimer");
        exit(EXIT_FAILURE);
    }
//    alarm_status = signal(SIGALRM, handler);//保存alarm信号处理函数原来的状态
//    alarm(1);
    atexit(mod_load); //退出时调用
}

//卸载信号处理模块 当发生异常退出时 可以将占用的资源释放 将alarm信号取消
static void mod_unload() {
//    signal(SIGALRM, alarm_status);
//    alarm(0);
    sigaction(SIGALRM, &oldact, NULL);
    struct itimerval timer;

    timer.it_interval.tv_sec = 0;
    timer.it_interval.tv_usec = 0;

    timer.it_value.tv_sec = 0;
    timer.it_value.tv_usec = 0;
    // 启动定时器
    if (setitimer(ITIMER_REAL, &timer, NULL) == -1) {
        perror("setitimer");
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < MYTBF_MAX; i++) {
        free(job[i]);
    }
}

mytbf_t *mytbf_init(int cps, int burst) {
    struct mytbf_st *tbf;

    if (!inited) {
        mod_load();
    }

    //将新的tbf装载到任务组中
    int pos;
    pos = get_free_pos();
    if (pos == -1) {
        return NULL;
    }

    tbf = malloc(sizeof(*tbf));
    if (tbf == NULL)
        return NULL;
    tbf->token = 0;
    tbf->csp = cps;
    tbf->burst = burst;
    tbf->pos = pos;

    job[pos] = tbf;

    return tbf;
}

//获取token ptr是一个 void * size是用户想要获取的token数
int mytbf_fetchtoken(mytbf_t *ptr, int size) {
    struct mytbf_st *tbf = ptr;

    if (size <= 0) {
        return -EINVAL;
    }

    //有token继续
    while (tbf->token <= 0)
        pause(); //使进程挂起,直到接收一个信号

    int n = tbf->token < size ? tbf->token : size;

    tbf->token -= n;
    //用户获取了 n 个token
    return n;
}

//归还token ptr是一个 void *
int mytbf_returntoken(mytbf_t *ptr, int size) {
    struct mytbf_st *tbf = ptr;

    if (size <= 0) {
        return -EINVAL;
    }

    tbf->token += size;
    if (tbf->token > tbf->burst)
        tbf->token = tbf->burst;

    return size;
}

int mytbf_destroy(mytbf_t *ptr) {
    struct mytbf_st *tbf = ptr;
    job[tbf->pos] = NULL;
    free(tbf);
    return 0;
}