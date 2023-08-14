/* Exported API */
void bioInit(void);

void bioCreateBackgroundJob(int type, void *arg1, void *arg2, void *arg3);

unsigned long long bioPendingJobsOfType(int type);

unsigned long long bioWaitStepOfType(int type);

time_t bioOlderJobOfType(int type);

void bioKillThreads(void);

/* Background job opcodes */
#define BIO_CLOSE_FILE    0 /* Deferred close(2) syscall. 文件关闭后台任务 */
#define BIO_AOF_FSYNC     1 /* Deferred AOF fsync.  AOF日志同步写回后台任务*/
#define BIO_LAZY_FREE     2 /* Deferred objects freeing. 惰性删除*/
#define BIO_NUM_OPS       3 //后台任务的类型有三种
