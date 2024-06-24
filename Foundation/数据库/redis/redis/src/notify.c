#include "server.h"

/* This file implements keyspace events notification via Pub/Sub and
 * described at https://redis.io/topics/notifications. */

/* Turn a string representing notification classes into an integer
 * representing notification classes flags xored.
 *
 * The function returns -1 if the input contains characters not mapping to
 * any class. */
int keyspaceEventsStringToFlags(char *classes) {
    char *p = classes;
    int c, flags = 0;

    while ((c = *p++) != '\0') {
        switch (c) {
            case 'A':
                flags |= NOTIFY_ALL;
                break;
            case 'g':
                flags |= NOTIFY_GENERIC;
                break;
            case '$':
                flags |= NOTIFY_STRING;
                break;
            case 'l':
                flags |= NOTIFY_LIST;
                break;
            case 's':
                flags |= NOTIFY_SET;
                break;
            case 'h':
                flags |= NOTIFY_HASH;
                break;
            case 'z':
                flags |= NOTIFY_ZSET;
                break;
            case 'x':
                flags |= NOTIFY_EXPIRED;
                break;
            case 'e':
                flags |= NOTIFY_EVICTED;
                break;
            case 'K':
                flags |= NOTIFY_KEYSPACE;
                break;
            case 'E':
                flags |= NOTIFY_KEYEVENT;
                break;
            case 't':
                flags |= NOTIFY_STREAM;
                break;
            default:
                return -1;
        }
    }
    return flags;
}

/* This function does exactly the revese of the function above: it gets
 * as input an integer with the xored flags and returns a string representing
 * the selected classes. The string returned is an sds string that needs to
 * be released with sdsfree(). */
sds keyspaceEventsFlagsToString(int flags) {
    sds res;

    res = sdsempty();
    if ((flags & NOTIFY_ALL) == NOTIFY_ALL) {
        res = sdscatlen(res, "A", 1);
    } else {
        if (flags & NOTIFY_GENERIC) res = sdscatlen(res, "g", 1);
        if (flags & NOTIFY_STRING) res = sdscatlen(res, "$", 1);
        if (flags & NOTIFY_LIST) res = sdscatlen(res, "l", 1);
        if (flags & NOTIFY_SET) res = sdscatlen(res, "s", 1);
        if (flags & NOTIFY_HASH) res = sdscatlen(res, "h", 1);
        if (flags & NOTIFY_ZSET) res = sdscatlen(res, "z", 1);
        if (flags & NOTIFY_EXPIRED) res = sdscatlen(res, "x", 1);
        if (flags & NOTIFY_EVICTED) res = sdscatlen(res, "e", 1);
        if (flags & NOTIFY_STREAM) res = sdscatlen(res, "t", 1);
    }
    if (flags & NOTIFY_KEYSPACE) res = sdscatlen(res, "K", 1);
    if (flags & NOTIFY_KEYEVENT) res = sdscatlen(res, "E", 1);
    return res;
}

/* The API provided to the rest of the Redis core is a simple function:
 *
 * notifyKeyspaceEvent(char *event, robj *key, int dbid);
 * 'type' 当前想要发送的通知的类型
 * 'event' 事件的名称
 * 'key' 产生事件的键
 * 'dbid'  产生事件的数据库号码  */
void notifyKeyspaceEvent(int type, char *event, robj *key, int dbid) {
    sds chan;
    robj *chanobj, *eventobj;
    int len = -1;
    char buf[24];

    /* If any modules are interested in events, notify the module system now. 
     * This bypasses the notifications configuration, but the module engine
     * will only call event subscribers if the event type matches the types
     * they are interested in. */
    moduleNotifyKeyspaceEvent(type, event, key, dbid);

    /* 如果给定的通知不是服务器允许发送的通知,直接return */
    if (!(server.notify_keyspace_events & type)) return;

    eventobj = createStringObject(event, strlen(event));

    /* __keyspace@<db>__:<key> <event> notifications. */
    //发送键空间通知
    if (server.notify_keyspace_events & NOTIFY_KEYSPACE) {
        chan = sdsnewlen("__keyspace@", 11);
        len = ll2string(buf, sizeof(buf), dbid);
        chan = sdscatlen(chan, buf, len);
        chan = sdscatlen(chan, "__:", 3);
        chan = sdscatsds(chan, key->ptr);//拼接频道名
        chanobj = createObject(OBJ_STRING, chan);
        pubsubPublishMessage(chanobj, eventobj); //发送通知
        decrRefCount(chanobj);
    }

    /* __keyevent@<db>__:<event> <key> notifications. */
    if (server.notify_keyspace_events & NOTIFY_KEYEVENT) {
        chan = sdsnewlen("__keyevent@", 11);
        if (len == -1) len = ll2string(buf, sizeof(buf), dbid);
        chan = sdscatlen(chan, buf, len);
        chan = sdscatlen(chan, "__:", 3);
        chan = sdscatsds(chan, eventobj->ptr);
        chanobj = createObject(OBJ_STRING, chan);
        pubsubPublishMessage(chanobj, key);
        decrRefCount(chanobj);
    }
    decrRefCount(eventobj);
}
