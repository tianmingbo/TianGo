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

/* File event structure */
typedef struct aeFileEvent {
    int mask; /* one of AE_(READABLE|WRITABLE|BARRIER) */
    aeFileProc *rfileProc; //AE_READABLE处理函数
    aeFileProc *wfileProc;//AE_WRITABLE处理函数
    void *clientData;
} aeFileEvent;

/* Time event structure */
typedef struct aeTimeEvent {
    long long id; /* 时间事件id */
    long when_sec; /* 事件到达的秒级时间戳 */
    long when_ms; /* 毫秒级 */
    aeTimeProc *timeProc; //事件触发后的处理函数
    aeEventFinalizerProc *finalizerProc; //事件结束后的处理函数
    void *clientData; //事件相关的私有属性
    struct aeTimeEvent *prev;//时间事件链表的前向指针
    struct aeTimeEvent *next;//时间事件链表的next指针
} aeTimeEvent;

/* A fired event */
typedef struct aeFiredEvent {
    int fd;
    int mask;
} aeFiredEvent;

/* State of an event based program */
typedef struct aeEventLoop {
    int maxfd;   /* highest file descriptor currently registered */
    int setsize; /* max number of file descriptors tracked */
    long long timeEventNextId;
    time_t lastTime;     /* Used to detect system clock skew */
    aeFileEvent *events; /* Registered events IO事件数组 */
    aeFiredEvent *fired; /* 记录已触发事件对应的文件描述符信息 */
    aeTimeEvent *timeEventHead; //记录时间事件的链表头
    int stop;
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
