#include "server.h"
#include "bio.h"

//保存线程描述符的数组
static pthread_t bio_threads[BIO_NUM_OPS];
//保存互斥锁的数组
static pthread_mutex_t bio_mutex[BIO_NUM_OPS];
//保存条件变量的两个数组
static pthread_cond_t bio_newjob_cond[BIO_NUM_OPS];
static pthread_cond_t bio_step_cond[BIO_NUM_OPS];
//以后台线程方式运行的任务列表
static list *bio_jobs[BIO_NUM_OPS];
//被阻塞的后台任务数组
static unsigned long long bio_pending[BIO_NUM_OPS];

/* This structure represents a background Job. It is only used locally to this
 * file as the API does not expose the internals at all. */
struct bio_job {
    time_t time; /* 任务创建时间 */
    /* Job specific arguments pointers. If we need to pass more than three
     * arguments we can just pass a pointer to a structure or alike. */
    void *arg1, *arg2, *arg3;
};

void *bioProcessBackgroundJobs(void *arg);

void lazyfreeFreeObjectFromBioThread(robj *o);

void lazyfreeFreeDatabaseFromBioThread(dict *ht1, dict *ht2);

void lazyfreeFreeSlotsMapFromBioThread(zskiplist *sl);

/* Make sure we have enough stack to perform all the things we do in the
 * main thread. */
#define REDIS_THREAD_STACK_SIZE (1024*1024*4)

/* 初始化后台线程 */
void bioInit(void) {
    pthread_attr_t attr;
    pthread_t thread;
    size_t stacksize;
    int j;

    /* Initialization of state vars and objects */
    for (j = 0; j < BIO_NUM_OPS; j++) {
        /*
         * pthread_mutex_init 函数用于对互斥量进行初始化操作。它接受两个参数：
         * mutex 是一个指向 pthread_mutex_t 类型的指针，用于指定要初始化的互斥量对象。
         * attr 是一个指向 pthread_mutexattr_t 类型的指针，用于指定互斥量的属性。如果传入 NULL，表示使用默认属性。
         * */
        pthread_mutex_init(&bio_mutex[j], NULL);
        /*
         * pthread_cond_init
         * 作用是初始化条件变量,主要参数包括:
         * cond: 条件变量指针,像初始化互斥锁那样,首先定义一个pthread_cond_t变量,然后传址调用初始化函数。
         * attr: 条件变量属性,通常设为NULL使用默认属性。
         * */

        pthread_cond_init(&bio_newjob_cond[j], NULL);
        pthread_cond_init(&bio_step_cond[j], NULL);
        // 创建任务队列
        bio_jobs[j] = listCreate();
        bio_pending[j] = 0;
    }

    /* 设置线程栈大小,避免在某些系统中线程栈太小导致出错 */
    pthread_attr_init(&attr); //初始化pthread属性对象attr
    pthread_attr_getstacksize(&attr, &stacksize); //获取attr当前的栈大小设置,存入stacksize变量
    if (!stacksize) stacksize = 1; /* 检查stacksize,如果为0则设为1 */
    //当stacksize小于REDIS_THREAD_STACK_SIZE时,循环将其乘2,直到大于等于所需栈大小 4MB
    while (stacksize < REDIS_THREAD_STACK_SIZE) stacksize *= 2;
    //设置attr的栈大小为调整后的stacksize
    pthread_attr_setstacksize(&attr, stacksize);

    /* 创建后台现场,并指定bioProcessBackgroundJobs为线程执行函数.arg指定了该线程负责执行的是哪一类后台任务 */
    for (j = 0; j < BIO_NUM_OPS; j++) {
        void *arg = (void *) (unsigned long) j;
        //创建三个线程,执行的函数都是bioProcessBackgroundJobs
        if (pthread_create(&thread, &attr, bioProcessBackgroundJobs, arg) != 0) {
            serverLog(LL_WARNING, "Fatal: Can't initialize Background Jobs.");
            exit(1);
        }
        bio_threads[j] = thread;
    }
}

/* 负责添加一个后台任务,该函数通常由主线程调用,
 * 非阻塞删除就是主线程调用该函数添加后台任务实现的. */
void bioCreateBackgroundJob(int type, void *arg1, void *arg2, void *arg3) {
    struct bio_job *job = zmalloc(sizeof(*job));
    // 每类任务最多可以附加3个参数,这些参数用于判断任务类型或者执行任务
    job->time = time(NULL);
    job->arg1 = arg1;
    job->arg2 = arg2;
    job->arg3 = arg3;
    // 抢占该类任务对应的互斥量,再将该任务添加到对应的任务队列中
    pthread_mutex_lock(&bio_mutex[type]);
    //把任务加到对应列表尾部
    listAddNodeTail(bio_jobs[type], job);
    //等待处理的任务个数+1
    bio_pending[type]++;
    /*
     * pthread_cond_signal:
     * 唤醒cond变量上当前正在等待的线程中的一个。
     * 如果没有线程等待该变量,信号会丢失。
     * 被唤醒的线程需要重新检查循环条件。
     * */
    pthread_cond_signal(&bio_newjob_cond[type]);
    // 释放互斥量
    pthread_mutex_unlock(&bio_mutex[type]);
}

// 负责执行后台任务的主逻辑
void *bioProcessBackgroundJobs(void *arg) {
    struct bio_job *job;
    //接收一个unsigned long类型的参数arg,type代表任务类型
    unsigned long type = (unsigned long) arg;
    sigset_t sigset;

    /* Check that the type is within the right interval. */
    if (type >= BIO_NUM_OPS) {
        serverLog(LL_WARNING,
                  "Warning: bio thread started with wrong type %lu", type);
        return NULL;
    }

    /* pthread_setcancelstate
     * 用于设置线程的取消状态。线程的取消状态决定了是否允许该线程被取消（终止）
     * PTHREAD_CANCEL_ENABLE：允许线程被取消。
     * PTHREAD_CANCEL_DISABLE：禁止线程被取消。
     * */
    pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
    /* pthread_setcanceltype
     * 设置线程的取消类型。线程的取消类型决定了在取消线程时如何进行清理处理。
     * PTHREAD_CANCEL_DEFERRED：线程的取消请求将被延迟处理，直到线程到达取消点时才会被取消。
     * PTHREAD_CANCEL_ASYNCHRONOUS：线程的取消请求将立即生效，无论线程当前是否处于取消点。
     * */
    pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, NULL);

    pthread_mutex_lock(&bio_mutex[type]); // 抢占该任务类型的互斥量
    /* 屏蔽SIGALRM信号,只让main thread处理 */
    sigemptyset(&sigset);
    sigaddset(&sigset, SIGALRM);
    if (pthread_sigmask(SIG_BLOCK, &sigset, NULL))
        serverLog(LL_WARNING,
                  "Warning: can't mask SIGALRM in bio.c thread: %s", strerror(errno));

    while (1) {
        listNode *ln;

        /* 检查当前任务队列中的任务是否为空,如果为空,
         * 则将当前线程阻塞在bio_newjob_cond条件变量上 */
        if (listLength(bio_jobs[type]) == 0) {
            pthread_cond_wait(&bio_newjob_cond[type], &bio_mutex[type]);
            continue;
        }
        /* 从类型为type的任务队列中获取第一个任务 */
        ln = listFirst(bio_jobs[type]);
        job = ln->value;
        /* 释放互斥量.在后台任务执行期间,后台线程是不锁定互斥量的,
         * 否则主线程在添加后台任务时可能会一直阻塞,这样后台线程就失去了意义. */
        pthread_mutex_unlock(&bio_mutex[type]);

        /* 处理不同类型的后台任务 */
        if (type == BIO_CLOSE_FILE) {
            close((long) job->arg1);
        } else if (type == BIO_AOF_FSYNC) {
            redis_fsync((long) job->arg1);
        } else if (type == BIO_LAZY_FREE) {
            /* What we free changes depending on what arguments are set:
             * arg1 -> free the object at pointer.
             * arg2 & arg3 -> free two dictionaries (a Redis DB).
             * only arg3 -> free the skiplist. */
            if (job->arg1)
                lazyfreeFreeObjectFromBioThread(job->arg1);
            else if (job->arg2 && job->arg3)
                lazyfreeFreeDatabaseFromBioThread(job->arg2, job->arg3);
            else if (job->arg3)
                lazyfreeFreeSlotsMapFromBioThread(job->arg3);
        } else {
            serverPanic("Wrong job type in bioProcessBackgroundJobs().");
        }
        zfree(job);

        /* Lock again before reiterating the loop, if there are no longer
         * jobs to process we'll block again in pthread_cond_wait(). */
        pthread_mutex_lock(&bio_mutex[type]);
        //任务执行完成后,在队列中删除该任务
        listDelNode(bio_jobs[type], ln);
        //对应的等待任务-1
        bio_pending[type]--;

        /* Unblock threads blocked on bioWaitStepOfType() if any. */
        pthread_cond_broadcast(&bio_step_cond[type]);
    }
}

/* Return the number of pending jobs of the specified type. */
unsigned long long bioPendingJobsOfType(int type) {
    unsigned long long val;
    pthread_mutex_lock(&bio_mutex[type]);
    val = bio_pending[type];
    pthread_mutex_unlock(&bio_mutex[type]);
    return val;
}

/* If there are pending jobs for the specified type, the function blocks
 * and waits that the next job was processed. Otherwise the function
 * does not block and returns ASAP.
 *
 * The function returns the number of jobs still to process of the
 * requested type.
 *
 * This function is useful when from another thread, we want to wait
 * a bio.c thread to do more work in a blocking way.
 */
unsigned long long bioWaitStepOfType(int type) {
    unsigned long long val;
    pthread_mutex_lock(&bio_mutex[type]);
    val = bio_pending[type];
    if (val != 0) {
        pthread_cond_wait(&bio_step_cond[type], &bio_mutex[type]);
        val = bio_pending[type];
    }
    pthread_mutex_unlock(&bio_mutex[type]);
    return val;
}

/* Kill the running bio threads in an unclean way. This function should be
 * used only when it's critical to stop the threads for some reason.
 * Currently Redis does this only on crash (for instance on SIGSEGV) in order
 * to perform a fast memory check without other threads messing with memory. */
void bioKillThreads(void) {
    int err, j;

    for (j = 0; j < BIO_NUM_OPS; j++) {
        if (pthread_cancel(bio_threads[j]) == 0) {
            if ((err = pthread_join(bio_threads[j], NULL)) != 0) {
                serverLog(LL_WARNING,
                          "Bio thread for job type #%d can be joined: %s",
                          j, strerror(err));
            } else {
                serverLog(LL_WARNING,
                          "Bio thread for job type #%d terminated", j);
            }
        }
    }
}
