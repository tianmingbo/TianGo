#ifndef __AE_H__
#define __AE_H__

#include <time.h>

#define AE_OK 0
#define AE_ERR -1

#define AE_NONE 0       /* No events registered. */
#define AE_READABLE 1   /* 可读事件 */
#define AE_WRITABLE 2   /* 可写事件 */
#define AE_BARRIER 4    /* With WRITABLE, never fire the event if the
                           READABLE event already fired in the same event
                           loop iteration. Useful when you want to persist
                           things to disk before sending replies, and want
                           to do that in a group fashion. */

#define AE_FILE_EVENTS 1
#define AE_TIME_EVENTS 2
#define AE_ALL_EVENTS (AE_FILE_EVENTS|AE_TIME_EVENTS)
#define AE_DONT_WAIT 4
#define AE_CALL_AFTER_SLEEP 8

#define AE_NOMORE -1
#define AE_DELETED_EVENT_ID -1

/* Macros */
#define AE_NOTUSED(V) ((void) V)

struct aeEventLoop;

/* Types and data structures */
typedef void aeFileProc(struct aeEventLoop *eventLoop, int fd, void *clientData, int mask);

typedef int aeTimeProc(struct aeEventLoop *eventLoop, long long id, void *clientData);

typedef void aeEventFinalizerProc(struct aeEventLoop *eventLoop, void *clientData);

typedef void aeBeforeSleepProc(struct aeEventLoop *eventLoop);

/* 存储了一个文件描述符上已注册的文件事件 */
typedef struct aeFileEvent {
    int mask; /* one of AE_(READABLE|WRITABLE|BARRIER) */
    aeFileProc *rfileProc; //AE_READABLE处理函数
    aeFileProc *wfileProc;//AE_WRITABLE处理函数
    void *clientData; //附加数据
} aeFileEvent;

/* 存储了一个时间事件的信息 */
typedef struct aeTimeEvent {
    long long id; /* 时间事件id */
    long when_sec; /* 事件到达的秒级时间戳 */
    long when_ms; /* 剩余毫秒级 */
    aeTimeProc *timeProc; //事件触发后的处理函数
    aeEventFinalizerProc *finalizerProc; //事件结束后的处理函数
    void *clientData; //事件相关的私有属性
    struct aeTimeEvent *prev;//时间事件链表的前向指针
    struct aeTimeEvent *next;//时间事件链表的next指针
} aeTimeEvent;

/* 已就绪的事件 */
typedef struct aeFiredEvent {
    int fd; //产生事件的文件描述符
    int mask; //产生的事件类型
} aeFiredEvent;

/* 时间循环器,负责管理事件 */
typedef struct aeEventLoop {
    int maxfd;   /* 当前已注册的最大文件描述符 */
    int setsize; /* 该事件循环器允许监听的最大的文件描述符 */
    long long timeEventNextId; //下一个时间事件ID
    time_t lastTime;     /* 上一次执行时间事件的时间,用于判断是否发生系统时间偏移 */
    aeFileEvent *events; /* 已注册的文件事件表,数组索引即文件描述符,数组元素即该文件描述符上注册的文件事件 */
    aeFiredEvent *fired; /* 已就绪的事件表 */
    aeTimeEvent *timeEventHead; //记录时间事件的链表头
    int stop; //事件循环器是否停止
    void *apidata; /* 和API调用接口相关的数据 */
    aeBeforeSleepProc *beforesleep; //进入事件循环流程前执行的函数
    aeBeforeSleepProc *aftersleep;
} aeEventLoop;

/* Prototypes */
aeEventLoop *aeCreateEventLoop(int setsize);

void aeDeleteEventLoop(aeEventLoop *eventLoop);

void aeStop(aeEventLoop *eventLoop);

int aeCreateFileEvent(aeEventLoop *eventLoop, int fd, int mask,
                      aeFileProc *proc, void *clientData);

void aeDeleteFileEvent(aeEventLoop *eventLoop, int fd, int mask);

int aeGetFileEvents(aeEventLoop *eventLoop, int fd);

long long aeCreateTimeEvent(aeEventLoop *eventLoop, long long milliseconds,
                            aeTimeProc *proc, void *clientData,
                            aeEventFinalizerProc *finalizerProc);

int aeDeleteTimeEvent(aeEventLoop *eventLoop, long long id);

int aeProcessEvents(aeEventLoop *eventLoop, int flags);

int aeWait(int fd, int mask, long long milliseconds);

void aeMain(aeEventLoop *eventLoop);

char *aeGetApiName(void);

void aeSetBeforeSleepProc(aeEventLoop *eventLoop, aeBeforeSleepProc *beforesleep);

void aeSetAfterSleepProc(aeEventLoop *eventLoop, aeBeforeSleepProc *aftersleep);

int aeGetSetSize(aeEventLoop *eventLoop);

int aeResizeSetSize(aeEventLoop *eventLoop, int setsize);

#endif
