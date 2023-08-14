/* Background I/O service for Redis.
 *
 * This file implements operations that we need to perform in the background.
 * Currently there is only a single operation, that is a background close(2)
 * system call. This is needed as when the process is the last owner of a
 * reference to a file closing it means unlinking it, and the deletion of the
 * file is slow, blocking the server.
 *
 * In the future we'll either continue implementing new things we need or
 * we'll switch to libeio. However there are probably long term uses for this
 * file as we may want to put here Redis specific background tasks (for instance
 * it is not impossible that we'll need a non blocking FLUSHDB/FLUSHALL
 * implementation).
 *
 * DESIGN
 * ------
 *
 * The design is trivial, we have a structure representing a job to perform
 * and a different thread and job queue for every job type.
 * Every thread waits for new jobs in its queue, and process every job
 * sequentially.
 *
 * Jobs of the same type are guaranteed to be processed from the least
 * recently inserted to the most recently inserted (older jobs processed
 * first).
 *
 * Currently there is no way for the creator of the job to be notified about
 * the completion of the operation, this will only be added when/if needed.
 *
 */


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

/* Initialize the background system, spawning the thread. */
void bioInit(void) {
    pthread_attr_t attr;
    pthread_t thread;
    size_t stacksize;
    int j;

    /* Initialization of state vars and objects */
    for (j = 0; j < BIO_NUM_OPS; j++) {
        pthread_mutex_init(&bio_mutex[j], NULL);
        /*
         * pthread_cond_init
         * 作用是初始化条件变量,主要参数包括:
         * cond: 条件变量指针,像初始化互斥锁那样,首先定义一个pthread_cond_t变量,然后传址调用初始化函数。
         * attr: 条件变量属性,通常设为NULL使用默认属性。
         * */

        pthread_cond_init(&bio_newjob_cond[j], NULL);
        pthread_cond_init(&bio_step_cond[j], NULL);
        bio_jobs[j] = listCreate();
        bio_pending[j] = 0;
    }

    /* Set the stack size as by default it may be small in some system */
    pthread_attr_init(&attr); //初始化pthread属性对象attr
    pthread_attr_getstacksize(&attr, &stacksize); //获取attr当前的栈大小设置,存入stacksize变量
    if (!stacksize) stacksize = 1; /* 检查stacksize,如果为0则设为1 */
    //当stacksize小于REDIS_THREAD_STACK_SIZE时,循环将其乘2,直到大于等于所需栈大小 4MB
    while (stacksize < REDIS_THREAD_STACK_SIZE) stacksize *= 2;
    //设置attr的栈大小为调整后的stacksize
    pthread_attr_setstacksize(&attr, stacksize);

    /* Ready to spawn our threads. We use the single argument the thread
     * function accepts in order to pass the job ID the thread is
     * responsible of. */
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

void bioCreateBackgroundJob(int type, void *arg1, void *arg2, void *arg3) {
    //创建新的任务
    struct bio_job *job = zmalloc(sizeof(*job));

    job->time = time(NULL);
    job->arg1 = arg1;
    job->arg2 = arg2;
    job->arg3 = arg3;
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
    pthread_mutex_unlock(&bio_mutex[type]);
}

void *bioProcessBackgroundJobs(void *arg) {
    struct bio_job *job;
    //接收一个unsigned long类型的参数arg,代表任务类型
    unsigned long type = (unsigned long) arg;
    sigset_t sigset;

    /* Check that the type is within the right interval. */
    if (type >= BIO_NUM_OPS) {
        serverLog(LL_WARNING,
                  "Warning: bio thread started with wrong type %lu", type);
        return NULL;
    }

    /* Make the thread killable at any time, so that bioKillThreads()
     * can work reliably. */
    pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
    pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, NULL);

    pthread_mutex_lock(&bio_mutex[type]); //加互斥锁
    /* 屏蔽SIGALRM信号,只让main thread处理 */
    sigemptyset(&sigset);
    sigaddset(&sigset, SIGALRM);
    if (pthread_sigmask(SIG_BLOCK, &sigset, NULL))
        serverLog(LL_WARNING,
                  "Warning: can't mask SIGALRM in bio.c thread: %s", strerror(errno));

    while (1) {
        listNode *ln;

        /* The loop always starts with the lock hold. */
        if (listLength(bio_jobs[type]) == 0) {
            pthread_cond_wait(&bio_newjob_cond[type], &bio_mutex[type]);
            continue;
        }
        /* 从类型为type的任务队列中获取第一个任务 */
        ln = listFirst(bio_jobs[type]);
        job = ln->value;
        /* It is now possible to unlock the background system as we know have
         * a stand alone job structure to process.*/
        pthread_mutex_unlock(&bio_mutex[type]);

        /* Process the job accordingly to its type. */
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
