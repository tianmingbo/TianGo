#include "server.h"
#include "atomicvar.h"
#include <sys/socket.h>
#include <sys/uio.h>
#include <math.h>
#include <ctype.h>

static void setProtocolError(const char *errstr, client *c);

/* Return the size consumed from the allocator, for the specified SDS string,
 * including internal fragmentation. This function is used in order to compute
 * the client output buffer size. */
size_t sdsZmallocSize(sds s) {
    void *sh = sdsAllocPtr(s);
    return zmalloc_size(sh);
}

/* Return the amount of memory used by the sds string at object->ptr
 * for a string object. */
size_t getStringObjectSdsUsedMemory(robj *o) {
    serverAssertWithInfo(NULL, o, o->type == OBJ_STRING);
    switch (o->encoding) {
        case OBJ_ENCODING_RAW:
            return sdsZmallocSize(o->ptr);
        case OBJ_ENCODING_EMBSTR:
            return zmalloc_size(o) - sizeof(robj);
        default:
            return 0; /* Just integer encoding for now. */
    }
}

/* Client.reply list dup and free methods. */
void *dupClientReplyValue(void *o) {
    clientReplyBlock *old = o;
    clientReplyBlock *buf = zmalloc(sizeof(clientReplyBlock) + old->size);
    memcpy(buf, o, sizeof(clientReplyBlock) + old->size);
    return buf;
}

void freeClientReplyValue(void *o) {
    zfree(o);
}

int listMatchObjects(void *a, void *b) {
    return equalStringObjects(a, b);
}

/* This function links the client to the global linked list of clients.
 * unlinkClient() does the opposite, among other things. */
void linkClient(client *c) {
    listAddNodeTail(server.clients, c);
    /* Note that we remember the linked list node where the client is stored,
     * this way removing the client in unlinkClient() will not require
     * a linear scan, but just a constant time operation. */
    c->client_list_node = listLast(server.clients);
    uint64_t id = htonu64(c->id);
    raxInsert(server.clients_index, (unsigned char *) &id, sizeof(id), c, NULL);
}

client *createClient(int fd) {
    client *c = zmalloc(sizeof(client));

    /* 传递 -1 作为 fd 可以创建一个未连接的客户端。
     * 这很有用，因为所有命令都需要在客户端上下文中执行。 当命令在其他上下文（例如 Lua 脚本）中执行时，我们需要一个非连接的客户端。
     * */
    if (fd != -1) {
        //将连接设置为非阻塞模式
        anetNonBlock(NULL, fd);
        //关闭TCP的Delay选项
        anetEnableTcpNoDelay(NULL, fd);
        if (server.tcpkeepalive)
            //开启TCP的keepalive选项
            anetKeepAlive(NULL, fd, server.tcpkeepalive);
        //创建客户端对已连接套接字的监听,一旦有客户端有请求发送到server,框架就会回调readQueryFromClient函数
        if (aeCreateFileEvent(server.el, fd, AE_READABLE,
                              readQueryFromClient, c) == AE_ERR) {
            close(fd);
            zfree(c);
            return NULL;
        }
    }
    //选择0号数据库
    selectDb(c, 0);
    uint64_t client_id;
    atomicGetIncr(server.next_client_id, client_id, 1);
    //初始化client属性
    c->id = client_id;
    c->fd = fd;
    c->name = NULL;
    c->bufpos = 0;
    c->qb_pos = 0;
    c->querybuf = sdsempty();
    c->pending_querybuf = sdsempty();
    c->querybuf_peak = 0;
    c->reqtype = 0;
    c->argc = 0;
    c->argv = NULL;
    c->cmd = c->lastcmd = NULL;
    c->multibulklen = 0;
    c->bulklen = -1;
    c->sentlen = 0;
    c->flags = 0;
    c->ctime = c->lastinteraction = server.unixtime;
    c->authenticated = 0;
    c->replstate = REPL_STATE_NONE;
    c->repl_put_online_on_ack = 0;
    c->reploff = 0;
    c->read_reploff = 0;
    c->repl_ack_off = 0;
    c->repl_ack_time = 0;
    c->slave_listening_port = 0;
    c->slave_ip[0] = '\0';
    c->slave_capa = SLAVE_CAPA_NONE;
    c->reply = listCreate();
    c->reply_bytes = 0;
    c->obuf_soft_limit_reached_time = 0;
    listSetFreeMethod(c->reply, freeClientReplyValue);
    listSetDupMethod(c->reply, dupClientReplyValue);
    c->btype = BLOCKED_NONE;
    c->bpop.timeout = 0;
    c->bpop.keys = dictCreate(&objectKeyHeapPointerValueDictType, NULL);
    c->bpop.target = NULL;
    c->bpop.xread_group = NULL;
    c->bpop.xread_consumer = NULL;
    c->bpop.xread_group_noack = 0;
    c->bpop.numreplicas = 0;
    c->bpop.reploffset = 0;
    c->woff = 0;
    c->watched_keys = listCreate();
    c->pubsub_channels = dictCreate(&objectKeyPointerValueDictType, NULL);
    c->pubsub_patterns = listCreate();
    c->peerid = NULL;
    c->client_list_node = NULL;
    listSetFreeMethod(c->pubsub_patterns, decrRefCountVoid);
    listSetMatchMethod(c->pubsub_patterns, listMatchObjects);
    //
    if (fd != -1) linkClient(c);
    initClientMultiState(c);
    return c;
}

/* 将客户端放入一个客户端队列中，这些客户端需要将其输出缓冲区的数据写入套接字，并将其标记为待写入的状态。 */
void clientInstallWriteHandler(client *c) {
    /* 如果客户端的 CLIENT_PENDING_WRITE 标志位未设置，
     * 并且客户端不处于复制状态（replstate 为 REPL_STATE_NONE），
     * 或者客户端是从服务器并且从服务器处于在线状态（SLAVE_STATE_ONLINE），
     * 且不需要等待从服务器确认 (repl_put_online_on_ack 未设置)。 */
    if (!(c->flags & CLIENT_PENDING_WRITE) &&
        (c->replstate == REPL_STATE_NONE ||
         (c->replstate == SLAVE_STATE_ONLINE && !c->repl_put_online_on_ack))) {
        /* 将客户端的 CLIENT_PENDING_WRITE 标志位置位，表示需要进行写操作 */
        c->flags |= CLIENT_PENDING_WRITE;
        // 将客户端节点添加到由服务器维护的客户端待写入队列（server.clients_pending_write）的头部。
        listAddNodeHead(server.clients_pending_write, c);
    }
}

/* This function is called every time we are going to transmit new data
 * to the client. The behavior is the following:
 *
 * If the client should receive new data (normal clients will) the function
 * returns C_OK, and make sure to install the write handler in our event
 * loop so that when the socket is writable new data gets written.
 *
 * If the client should not receive new data, because it is a fake client
 * (used to load AOF in memory), a master or because the setup of the write
 * handler failed, the function returns C_ERR.
 *
 * The function may return C_OK without actually installing the write
 * event handler in the following cases:
 *
 * 1) The event handler should already be installed since the output buffer
 *    already contains something.
 * 2) The client is a slave but not yet online, so we want to just accumulate
 *    writes in the buffer but not actually sending them yet.
 *
 * Typically gets called every time a reply is built, before adding more
 * data to the clients output buffers. If the function returns C_ERR no
 * data should be appended to the output buffers. */
int prepareClientToWrite(client *c) {
    /* If it's the Lua client we always return ok without installing any
     * handler since there is no socket at all. */
    if (c->flags & (CLIENT_LUA | CLIENT_MODULE)) return C_OK;

    /* CLIENT REPLY OFF / SKIP handling: don't send replies. */
    if (c->flags & (CLIENT_REPLY_OFF | CLIENT_REPLY_SKIP)) return C_ERR;

    /* Masters don't receive replies, unless CLIENT_MASTER_FORCE_REPLY flag
     * is set. */
    if ((c->flags & CLIENT_MASTER) &&
        !(c->flags & CLIENT_MASTER_FORCE_REPLY))
        return C_ERR;

    if (c->fd <= 0) return C_ERR; /* Fake client for AOF loading. */

    /* Schedule the client to write the output buffers to the socket, unless
     * it should already be setup to do so (it has already pending data). */
    if (!clientHasPendingReplies(c)) clientInstallWriteHandler(c);

    /* Authorize the caller to queue in the output buffer of this client. */
    return C_OK;
}

/* -----------------------------------------------------------------------------
 * Low level functions to add more data to output buffers.
 * -------------------------------------------------------------------------- */

int _addReplyToBuffer(client *c, const char *s, size_t len) {
    size_t available = sizeof(c->buf) - c->bufpos;

    if (c->flags & CLIENT_CLOSE_AFTER_REPLY) return C_OK;

    /* If there already are entries in the reply list, we cannot
     * add anything more to the static buffer. */
    if (listLength(c->reply) > 0) return C_ERR;

    /* Check that the buffer has enough space available for this string. */
    if (len > available) return C_ERR;

    memcpy(c->buf + c->bufpos, s, len);
    c->bufpos += len;
    return C_OK;
}

void _addReplyStringToList(client *c, const char *s, size_t len) {
    if (c->flags & CLIENT_CLOSE_AFTER_REPLY) return;

    listNode *ln = listLast(c->reply);
    clientReplyBlock *tail = ln ? listNodeValue(ln) : NULL;

    /* Note that 'tail' may be NULL even if we have a tail node, becuase when
     * addDeferredMultiBulkLength() is used, it sets a dummy node to NULL just
     * fo fill it later, when the size of the bulk length is set. */

    /* Append to tail string when possible. */
    if (tail) {
        /* Copy the part we can fit into the tail, and leave the rest for a
         * new node */
        size_t avail = tail->size - tail->used;
        size_t copy = avail >= len ? len : avail;
        memcpy(tail->buf + tail->used, s, copy);
        tail->used += copy;
        s += copy;
        len -= copy;
    }
    if (len) {
        /* Create a new node, make sure it is allocated to at
         * least PROTO_REPLY_CHUNK_BYTES */
        size_t size = len < PROTO_REPLY_CHUNK_BYTES ? PROTO_REPLY_CHUNK_BYTES : len;
        tail = zmalloc(size + sizeof(clientReplyBlock));
        /* take over the allocation's internal fragmentation */
        tail->size = zmalloc_usable(tail) - sizeof(clientReplyBlock);
        tail->used = len;
        memcpy(tail->buf, s, len);
        listAddNodeTail(c->reply, tail);
        c->reply_bytes += tail->size;
    }
    asyncCloseClientOnOutputBufferLimitReached(c);
}

/* -----------------------------------------------------------------------------
 * Higher level functions to queue data on the client output buffer.
 * The following functions are the ones that commands implementations will call.
 * -------------------------------------------------------------------------- */

/* Add the object 'obj' string representation to the client output buffer. */
void addReply(client *c, robj *obj) {
    if (prepareClientToWrite(c) != C_OK) return;

    if (sdsEncodedObject(obj)) {
        // 先尝试写入client.buf,如果写不下,则写入client.reply
        if (_addReplyToBuffer(c, obj->ptr, sdslen(obj->ptr)) != C_OK)
            _addReplyStringToList(c, obj->ptr, sdslen(obj->ptr));
    } else if (obj->encoding == OBJ_ENCODING_INT) {
        /* For integer encoded strings we just convert it into a string
         * using our optimized function, and attach the resulting string
         * to the output buffer. */
        char buf[32];
        size_t len = ll2string(buf, sizeof(buf), (long) obj->ptr);
        if (_addReplyToBuffer(c, buf, len) != C_OK)
            _addReplyStringToList(c, buf, len);
    } else {
        serverPanic("Wrong obj->encoding in addReply()");
    }
}

/* Add the SDS 's' string to the client output buffer, as a side effect
 * the SDS string is freed. */
void addReplySds(client *c, sds s) {
    if (prepareClientToWrite(c) != C_OK) {
        /* The caller expects the sds to be free'd. */
        sdsfree(s);
        return;
    }
    if (_addReplyToBuffer(c, s, sdslen(s)) != C_OK)
        _addReplyStringToList(c, s, sdslen(s));
    sdsfree(s);
}

/* This low level function just adds whatever protocol you send it to the
 * client buffer, trying the static buffer initially, and using the string
 * of objects if not possible.
 *
 * It is efficient because does not create an SDS object nor an Redis object
 * if not needed. The object will only be created by calling
 * _addReplyStringToList() if we fail to extend the existing tail object
 * in the list of objects. */
void addReplyString(client *c, const char *s, size_t len) {
    if (prepareClientToWrite(c) != C_OK) return;
    if (_addReplyToBuffer(c, s, len) != C_OK)
        _addReplyStringToList(c, s, len);
}

/* Low level function called by the addReplyError...() functions.
 * It emits the protocol for a Redis error, in the form:
 *
 * -ERRORCODE Error Message<CR><LF>
 *
 * If the error code is already passed in the string 's', the error
 * code provided is used, otherwise the string "-ERR " for the generic
 * error code is automatically added. */
void addReplyErrorLength(client *c, const char *s, size_t len) {
    /* If the string already starts with "-..." then the error code
     * is provided by the caller. Otherwise we use "-ERR". */
    if (!len || s[0] != '-') addReplyString(c, "-ERR ", 5);
    addReplyString(c, s, len);
    addReplyString(c, "\r\n", 2);

    /* Sometimes it could be normal that a slave replies to a master with
     * an error and this function gets called. Actually the error will never
     * be sent because addReply*() against master clients has no effect...
     * A notable example is:
     *
     *    EVAL 'redis.call("incr",KEYS[1]); redis.call("nonexisting")' 1 x
     *
     * Where the master must propagate the first change even if the second
     * will produce an error. However it is useful to log such events since
     * they are rare and may hint at errors in a script or a bug in Redis. */
    if (c->flags & (CLIENT_MASTER | CLIENT_SLAVE) && !(c->flags & CLIENT_MONITOR)) {
        char *to = c->flags & CLIENT_MASTER ? "master" : "replica";
        char *from = c->flags & CLIENT_MASTER ? "replica" : "master";
        char *cmdname = c->lastcmd ? c->lastcmd->name : "<unknown>";
        serverLog(LL_WARNING, "== CRITICAL == This %s is sending an error "
                              "to its %s: '%s' after processing the command "
                              "'%s'", from, to, s, cmdname);
    }
}

void addReplyError(client *c, const char *err) {
    addReplyErrorLength(c, err, strlen(err));
}

void addReplyErrorFormat(client *c, const char *fmt, ...) {
    size_t l, j;
    va_list ap;
    va_start(ap, fmt);
    sds s = sdscatvprintf(sdsempty(), fmt, ap);
    va_end(ap);
    /* Make sure there are no newlines in the string, otherwise invalid protocol
     * is emitted. */
    l = sdslen(s);
    for (j = 0; j < l; j++) {
        if (s[j] == '\r' || s[j] == '\n') s[j] = ' ';
    }
    addReplyErrorLength(c, s, sdslen(s));
    sdsfree(s);
}

void addReplyStatusLength(client *c, const char *s, size_t len) {
    addReplyString(c, "+", 1);
    addReplyString(c, s, len);
    addReplyString(c, "\r\n", 2);
}

void addReplyStatus(client *c, const char *status) {
    addReplyStatusLength(c, status, strlen(status));
}

void addReplyStatusFormat(client *c, const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    sds s = sdscatvprintf(sdsempty(), fmt, ap);
    va_end(ap);
    addReplyStatusLength(c, s, sdslen(s));
    sdsfree(s);
}

/* Adds an empty object to the reply list that will contain the multi bulk
 * length, which is not known when this function is called. */
void *addDeferredMultiBulkLength(client *c) {
    /* Note that we install the write event here even if the object is not
     * ready to be sent, since we are sure that before returning to the
     * event loop setDeferredMultiBulkLength() will be called. */
    if (prepareClientToWrite(c) != C_OK) return NULL;
    listAddNodeTail(c->reply, NULL); /* NULL is our placeholder. */
    return listLast(c->reply);
}

/* Populate the length object and try gluing it to the next chunk. */
void setDeferredMultiBulkLength(client *c, void *node, long length) {
    listNode *ln = (listNode *) node;
    clientReplyBlock *next;
    char lenstr[128];
    size_t lenstr_len = sprintf(lenstr, "*%ld\r\n", length);

    /* Abort when *node is NULL: when the client should not accept writes
     * we return NULL in addDeferredMultiBulkLength() */
    if (node == NULL) return;
    serverAssert(!listNodeValue(ln));

    /* Normally we fill this dummy NULL node, added by addDeferredMultiBulkLength(),
     * with a new buffer structure containing the protocol needed to specify
     * the length of the array following. However sometimes when there is
     * little memory to move, we may instead remove this NULL node, and prefix
     * our protocol in the node immediately after to it, in order to save a
     * write(2) syscall later. Conditions needed to do it:
     *
     * - The next node is non-NULL,
     * - It has enough room already allocated
     * - And not too large (avoid large memmove) */
    if (ln->next != NULL && (next = listNodeValue(ln->next)) &&
        next->size - next->used >= lenstr_len &&
        next->used < PROTO_REPLY_CHUNK_BYTES * 4) {
        memmove(next->buf + lenstr_len, next->buf, next->used);
        memcpy(next->buf, lenstr, lenstr_len);
        next->used += lenstr_len;
        listDelNode(c->reply, ln);
    } else {
        /* Create a new node */
        clientReplyBlock *buf = zmalloc(lenstr_len + sizeof(clientReplyBlock));
        /* Take over the allocation's internal fragmentation */
        buf->size = zmalloc_usable(buf) - sizeof(clientReplyBlock);
        buf->used = lenstr_len;
        memcpy(buf->buf, lenstr, lenstr_len);
        listNodeValue(ln) = buf;
        c->reply_bytes += buf->size;
    }
    asyncCloseClientOnOutputBufferLimitReached(c);
}

/* Add a double as a bulk reply */
void addReplyDouble(client *c, double d) {
    char dbuf[128], sbuf[128];
    int dlen, slen;
    if (isinf(d)) {
        /* Libc in odd systems (Hi Solaris!) will format infinite in a
         * different way, so better to handle it in an explicit way. */
        addReplyBulkCString(c, d > 0 ? "inf" : "-inf");
    } else {
        dlen = snprintf(dbuf, sizeof(dbuf), "%.17g", d);
        slen = snprintf(sbuf, sizeof(sbuf), "$%d\r\n%s\r\n", dlen, dbuf);
        addReplyString(c, sbuf, slen);
    }
}

/* Add a long double as a bulk reply, but uses a human readable formatting
 * of the double instead of exposing the crude behavior of doubles to the
 * dear user. */
void addReplyHumanLongDouble(client *c, long double d) {
    robj *o = createStringObjectFromLongDouble(d, 1);
    addReplyBulk(c, o);
    decrRefCount(o);
}

/* Add a long long as integer reply or bulk len / multi bulk count.
 * Basically this is used to output <prefix><long long><crlf>. */
void addReplyLongLongWithPrefix(client *c, long long ll, char prefix) {
    char buf[128];
    int len;

    /* Things like $3\r\n or *2\r\n are emitted very often by the protocol
     * so we have a few shared objects to use if the integer is small
     * like it is most of the times. */
    if (prefix == '*' && ll < OBJ_SHARED_BULKHDR_LEN && ll >= 0) {
        addReply(c, shared.mbulkhdr[ll]);
        return;
    } else if (prefix == '$' && ll < OBJ_SHARED_BULKHDR_LEN && ll >= 0) {
        addReply(c, shared.bulkhdr[ll]);
        return;
    }

    buf[0] = prefix;
    len = ll2string(buf + 1, sizeof(buf) - 1, ll);
    buf[len + 1] = '\r';
    buf[len + 2] = '\n';
    addReplyString(c, buf, len + 3);
}

void addReplyLongLong(client *c, long long ll) {
    if (ll == 0)
        addReply(c, shared.czero);
    else if (ll == 1)
        addReply(c, shared.cone);
    else
        addReplyLongLongWithPrefix(c, ll, ':');
}

void addReplyMultiBulkLen(client *c, long length) {
    if (length < OBJ_SHARED_BULKHDR_LEN)
        addReply(c, shared.mbulkhdr[length]);
    else
        addReplyLongLongWithPrefix(c, length, '*');
}

/* Create the length prefix of a bulk reply, example: $2234 */
void addReplyBulkLen(client *c, robj *obj) {
    size_t len;

    if (sdsEncodedObject(obj)) {
        len = sdslen(obj->ptr);
    } else {
        long n = (long) obj->ptr;

        /* Compute how many bytes will take this integer as a radix 10 string */
        len = 1;
        if (n < 0) {
            len++;
            n = -n;
        }
        while ((n = n / 10) != 0) {
            len++;
        }
    }

    if (len < OBJ_SHARED_BULKHDR_LEN)
        addReply(c, shared.bulkhdr[len]);
    else
        addReplyLongLongWithPrefix(c, len, '$');
}

/* Add a Redis Object as a bulk reply */
void addReplyBulk(client *c, robj *obj) {
    addReplyBulkLen(c, obj);
    addReply(c, obj);
    addReply(c, shared.crlf);
}

/* Add a C buffer as bulk reply */
void addReplyBulkCBuffer(client *c, const void *p, size_t len) {
    addReplyLongLongWithPrefix(c, len, '$');
    addReplyString(c, p, len);
    addReply(c, shared.crlf);
}

/* Add sds to reply (takes ownership of sds and frees it) */
void addReplyBulkSds(client *c, sds s) {
    addReplyLongLongWithPrefix(c, sdslen(s), '$');
    addReplySds(c, s);
    addReply(c, shared.crlf);
}

/* Add a C null term string as bulk reply */
void addReplyBulkCString(client *c, const char *s) {
    if (s == NULL) {
        addReply(c, shared.nullbulk);
    } else {
        addReplyBulkCBuffer(c, s, strlen(s));
    }
}

/* Add a long long as a bulk reply */
void addReplyBulkLongLong(client *c, long long ll) {
    char buf[64];
    int len;

    len = ll2string(buf, 64, ll);
    addReplyBulkCBuffer(c, buf, len);
}

/* Add an array of C strings as status replies with a heading.
 * This function is typically invoked by from commands that support
 * subcommands in response to the 'help' subcommand. The help array
 * is terminated by NULL sentinel. */
void addReplyHelp(client *c, const char **help) {
    sds cmd = sdsnew((char *) c->argv[0]->ptr);
    void *blenp = addDeferredMultiBulkLength(c);
    int blen = 0;

    sdstoupper(cmd);
    addReplyStatusFormat(c,
                         "%s <subcommand> arg arg ... arg. Subcommands are:", cmd);
    sdsfree(cmd);

    while (help[blen]) addReplyStatus(c, help[blen++]);

    blen++;  /* Account for the header line(s). */
    setDeferredMultiBulkLength(c, blenp, blen);
}

/* Add a suggestive error reply.
 * This function is typically invoked by from commands that support
 * subcommands in response to an unknown subcommand or argument error. */
void addReplySubcommandSyntaxError(client *c) {
    sds cmd = sdsnew((char *) c->argv[0]->ptr);
    sdstoupper(cmd);
    addReplyErrorFormat(c,
                        "Unknown subcommand or wrong number of arguments for '%s'. Try %s HELP.",
                        (char *) c->argv[1]->ptr, cmd);
    sdsfree(cmd);
}

/* Append 'src' client output buffers into 'dst' client output buffers. 
 * This function clears the output buffers of 'src' */
void AddReplyFromClient(client *dst, client *src) {
    if (prepareClientToWrite(dst) != C_OK)
        return;
    addReplyString(dst, src->buf, src->bufpos);
    if (listLength(src->reply))
        listJoin(dst->reply, src->reply);
    dst->reply_bytes += src->reply_bytes;
    src->reply_bytes = 0;
    src->bufpos = 0;
}

/* Copy 'src' client output buffers into 'dst' client output buffers.
 * The function takes care of freeing the old output buffers of the
 * destination client. */
void copyClientOutputBuffer(client *dst, client *src) {
    listRelease(dst->reply);
    dst->sentlen = 0;
    dst->reply = listDup(src->reply);
    memcpy(dst->buf, src->buf, src->bufpos);
    dst->bufpos = src->bufpos;
    dst->reply_bytes = src->reply_bytes;
}

/* Return true if the specified client has pending reply buffers to write to
 * the socket. */
int clientHasPendingReplies(client *c) {
    return c->bufpos || listLength(c->reply);
}

#define MAX_ACCEPTS_PER_CALL 1000

/*
 * 执行连接后的逻辑,如创建client结构体,为数据套接字注册文件事件回调函数
 * */
static void acceptCommonHandler(int fd, int flags, char *ip) {
    // 创建一个客户端
    client *c;
    if ((c = createClient(fd)) == NULL) {
        //如果创建失败
        serverLog(LL_WARNING, "Error registering fd event for the new client: %s (fd=%d)",
                  strerror(errno), fd);
        close(fd); /* May be already closed, just ignore errors */
        return;
    }
    // 如果超过最大连接数,关闭新连接
    if (listLength(server.clients) > server.maxclients) {
        char *err = "-ERR max number of clients reached\r\n";

        /* That's a best effort error message, don't check write errors */
        if (write(c->fd, err, strlen(err)) == -1) {
            /* Nothing to do, Just to avoid the warning... */
        }
        server.stat_rejected_conn++;
        freeClient(c);
        return;
    }

    /* If the server is running in protected mode (the default) and there
     * is no password set, nor a specific interface is bound, we don't accept
     * requests from non loopback interfaces. Instead we try to explain the
     * user what to do to fix it if needed. */
    if (server.protected_mode &&
        server.bindaddr_count == 0 &&
        server.requirepass == NULL &&
        !(flags & CLIENT_UNIX_SOCKET) &&
        ip != NULL) {
        if (strcmp(ip, "127.0.0.1") && strcmp(ip, "::1")) {
            char *err =
                    "-DENIED Redis is running in protected mode because protected "
                    "mode is enabled, no bind address was specified, no "
                    "authentication password is requested to clients. In this mode "
                    "connections are only accepted from the loopback interface. "
                    "If you want to connect from external computers to Redis you "
                    "may adopt one of the following solutions: "
                    "1) Just disable protected mode sending the command "
                    "'CONFIG SET protected-mode no' from the loopback interface "
                    "by connecting to Redis from the same host the server is "
                    "running, however MAKE SURE Redis is not publicly accessible "
                    "from internet if you do so. Use CONFIG REWRITE to make this "
                    "change permanent. "
                    "2) Alternatively you can just disable the protected mode by "
                    "editing the Redis configuration file, and setting the protected "
                    "mode option to 'no', and then restarting the server. "
                    "3) If you started the server manually just for testing, restart "
                    "it with the '--protected-mode no' option. "
                    "4) Setup a bind address or an authentication password. "
                    "NOTE: You only need to do one of the above things in order for "
                    "the server to start accepting connections from the outside.\r\n";
            if (write(c->fd, err, strlen(err)) == -1) {
                /* Nothing to do, Just to avoid the warning... */
            }
            server.stat_rejected_conn++;
            freeClient(c);
            return;
        }
    }
    // 连接数增加
    server.stat_numconnections++;
    c->flags |= flags;
}

void acceptTcpHandler(aeEventLoop *el, int fd, void *privdata, int mask) {
    int cport, cfd, max = MAX_ACCEPTS_PER_CALL;
    char cip[NET_IP_STR_LEN];
    // 忽略不使用的参数
    UNUSED(el);
    UNUSED(mask);
    UNUSED(privdata);
    //每次事件循环最多接受MAX_ACCEPTS_PER_CALL个请求,防止短时间内处理过多客户端导致进程阻塞
    while (max--) {
        // 调用anetTcpAccept接收新连接
        cfd = anetTcpAccept(server.neterr, fd, cip, sizeof(cip), &cport);
        if (cfd == ANET_ERR) {
            if (errno != EWOULDBLOCK)
                serverLog(LL_WARNING, "Accepting client connection: %s", server.neterr);
            return;
        }
        serverLog(LL_VERBOSE, "Accepted %s:%d", cip, cport);
        acceptCommonHandler(cfd, 0, cip);
    }
}

void acceptUnixHandler(aeEventLoop *el, int fd, void *privdata, int mask) {
    int cfd, max = MAX_ACCEPTS_PER_CALL;
    UNUSED(el);
    UNUSED(mask);
    UNUSED(privdata);

    while (max--) {
        cfd = anetUnixAccept(server.neterr, fd);
        if (cfd == ANET_ERR) {
            if (errno != EWOULDBLOCK)
                serverLog(LL_WARNING,
                          "Accepting client connection: %s", server.neterr);
            return;
        }
        serverLog(LL_VERBOSE, "Accepted connection to %s", server.unixsocket);
        acceptCommonHandler(cfd, CLIENT_UNIX_SOCKET, NULL);
    }
}

static void freeClientArgv(client *c) {
    int j;
    for (j = 0; j < c->argc; j++)
        decrRefCount(c->argv[j]);
    c->argc = 0;
    c->cmd = NULL;
}

/* 断开实例的所有从服务器连接 */
void disconnectSlaves(void) {
    while (listLength(server.slaves)) {
        listNode *ln = listFirst(server.slaves);
        freeClient((client *) ln->value);
    }
}

/* Remove the specified client from global lists where the client could
 * be referenced, not including the Pub/Sub channels.
 * This is used by freeClient() and replicationCacheMaster(). */
void unlinkClient(client *c) {
    listNode *ln;

    /* If this is marked as current client unset it. */
    if (server.current_client == c) server.current_client = NULL;

    /* Certain operations must be done only if the client has an active socket.
     * If the client was already unlinked or if it's a "fake client" the
     * fd is already set to -1. */
    if (c->fd != -1) {
        /* Remove from the list of active clients. */
        if (c->client_list_node) {
            uint64_t id = htonu64(c->id);
            raxRemove(server.clients_index, (unsigned char *) &id, sizeof(id), NULL);
            listDelNode(server.clients, c->client_list_node);
            c->client_list_node = NULL;
        }

        /* In the case of diskless replication the fork is writing to the
         * sockets and just closing the fd isn't enough, if we don't also
         * shutdown the socket the fork will continue to write to the slave
         * and the salve will only find out that it was disconnected when
         * it will finish reading the rdb. */
        if ((c->flags & CLIENT_SLAVE) &&
            (c->replstate == SLAVE_STATE_WAIT_BGSAVE_END)) {
            shutdown(c->fd, SHUT_RDWR);
        }

        /* Unregister async I/O handlers and close the socket. */
        aeDeleteFileEvent(server.el, c->fd, AE_READABLE);
        aeDeleteFileEvent(server.el, c->fd, AE_WRITABLE);
        close(c->fd);
        c->fd = -1;
    }

    /* Remove from the list of pending writes if needed. */
    if (c->flags & CLIENT_PENDING_WRITE) {
        ln = listSearchKey(server.clients_pending_write, c);
        serverAssert(ln != NULL);
        listDelNode(server.clients_pending_write, ln);
        c->flags &= ~CLIENT_PENDING_WRITE;
    }

    /* When client was just unblocked because of a blocking operation,
     * remove it from the list of unblocked clients. */
    if (c->flags & CLIENT_UNBLOCKED) {
        ln = listSearchKey(server.unblocked_clients, c);
        serverAssert(ln != NULL);
        listDelNode(server.unblocked_clients, ln);
        c->flags &= ~CLIENT_UNBLOCKED;
    }
}

void freeClient(client *c) {
    listNode *ln;

    /* 调用freeClientAsync将客户端添加到server.clients_to_close中 */
    if (c->flags & CLIENT_PROTECTED) {
        freeClientAsync(c);
        return;
    }

    /* 如果客户端是主节点客户端,则缓存该客户端信息,并将主从状态转换为待连接状态,
     * 以便后续与主节点重新建立连接
     * */
    if (server.master && c->flags & CLIENT_MASTER) {
        serverLog(LL_WARNING, "Connection with master lost.");
        if (!(c->flags & (CLIENT_CLOSE_AFTER_REPLY |
                          CLIENT_CLOSE_ASAP |
                          CLIENT_BLOCKED))) {
            replicationCacheMaster(c);
            return;
        }
    }

    /* Log link disconnection with slave */
    if ((c->flags & CLIENT_SLAVE) && !(c->flags & CLIENT_MONITOR)) {
        serverLog(LL_WARNING, "Connection with replica %s lost.",
                  replicationGetSlaveName(c));
    }

    /* Free the query buffer */
    sdsfree(c->querybuf);
    sdsfree(c->pending_querybuf);
    c->querybuf = NULL;

    /* Deallocate structures used to block on blocking ops. */
    if (c->flags & CLIENT_BLOCKED) unblockClient(c);
    dictRelease(c->bpop.keys);

    /* UNWATCH all the keys */
    unwatchAllKeys(c);
    listRelease(c->watched_keys);

    /* 取消所有的Pub/Sub订阅 */
    pubsubUnsubscribeAllChannels(c, 0);
    pubsubUnsubscribeAllPatterns(c, 0);
    dictRelease(c->pubsub_channels);
    listRelease(c->pubsub_patterns);

    /* Free data structures. */
    listRelease(c->reply);
    freeClientArgv(c);

    /* Unlink the client: this will close the socket, remove the I/O
     * handlers, and remove references of the client from different
     * places where active clients may be referenced. */
    unlinkClient(c);

    /* Master/slave cleanup Case 1:
     * we lost the connection with a slave. */
    if (c->flags & CLIENT_SLAVE) {
        if (c->replstate == SLAVE_STATE_SEND_BULK) {
            if (c->repldbfd != -1) close(c->repldbfd);
            if (c->replpreamble) sdsfree(c->replpreamble);
        }
        list *l = (c->flags & CLIENT_MONITOR) ? server.monitors : server.slaves;
        ln = listSearchKey(l, c);
        serverAssert(ln != NULL);
        listDelNode(l, ln);
        /* We need to remember the time when we started to have zero
         * attached slaves, as after some time we'll free the replication
         * backlog. */
        if (getClientType(c) == CLIENT_TYPE_SLAVE && listLength(server.slaves) == 0)
            server.repl_no_slaves_since = server.unixtime;
        refreshGoodSlavesCount();
    }

    /* Master/slave cleanup Case 2:
     * we lost the connection with the master. */
    if (c->flags & CLIENT_MASTER) replicationHandleMasterDisconnection();

    /* If this client was scheduled for async freeing we need to remove it
     * from the queue. */
    if (c->flags & CLIENT_CLOSE_ASAP) {
        ln = listSearchKey(server.clients_to_close, c);
        serverAssert(ln != NULL);
        listDelNode(server.clients_to_close, ln);
    }

    /* Release other dynamically allocated client structure fields,
     * and finally release the client structure itself. */
    if (c->name) decrRefCount(c->name);
    zfree(c->argv);
    freeClientMultiState(c);
    sdsfree(c->peerid);
    zfree(c);
}

/* Schedule a client to free it at a safe time in the serverCron() function.
 * This function is useful when we need to terminate a client but we are in
 * a context where calling freeClient() is not possible, because the client
 * should be valid for the continuation of the flow of the program. */
void freeClientAsync(client *c) {
    if (c->flags & CLIENT_CLOSE_ASAP || c->flags & CLIENT_LUA) return;
    c->flags |= CLIENT_CLOSE_ASAP;
    listAddNodeTail(server.clients_to_close, c);
}

void freeClientsInAsyncFreeQueue(void) {
    while (listLength(server.clients_to_close)) {
        listNode *ln = listFirst(server.clients_to_close);
        client *c = listNodeValue(ln);

        c->flags &= ~CLIENT_CLOSE_ASAP;
        freeClient(c);
        listDelNode(server.clients_to_close, ln);
    }
}

/* Return a client by ID, or NULL if the client ID is not in the set
 * of registered clients. Note that "fake clients", created with -1 as FD,
 * are not registered clients. */
client *lookupClientByID(uint64_t id) {
    id = htonu64(id);
    client *c = raxFind(server.clients_index, (unsigned char *) &id, sizeof(id));
    return (c == raxNotFound) ? NULL : c;
}

/* Write data in output buffers to client. Return C_OK if the client
 * is still valid after the call, C_ERR if it was freed. */
int writeToClient(int fd, client *c, int handler_installed) {
    ssize_t nwritten = 0, totwritten = 0;
    size_t objlen;
    clientReplyBlock *o;

    while (clientHasPendingReplies(c)) {
        if (c->bufpos > 0) {
            nwritten = write(fd, c->buf + c->sentlen, c->bufpos - c->sentlen);
            if (nwritten <= 0) break;
            c->sentlen += nwritten;
            totwritten += nwritten;

            /* If the buffer was sent, set bufpos to zero to continue with
             * the remainder of the reply. */
            if ((int) c->sentlen == c->bufpos) {
                c->bufpos = 0;
                c->sentlen = 0;
            }
        } else {
            o = listNodeValue(listFirst(c->reply));
            objlen = o->used;

            if (objlen == 0) {
                c->reply_bytes -= o->size;
                listDelNode(c->reply, listFirst(c->reply));
                continue;
            }

            nwritten = write(fd, o->buf + c->sentlen, objlen - c->sentlen);
            if (nwritten <= 0) break;
            c->sentlen += nwritten;
            totwritten += nwritten;

            /* If we fully sent the object on head go to the next one */
            if (c->sentlen == objlen) {
                c->reply_bytes -= o->size;
                listDelNode(c->reply, listFirst(c->reply));
                c->sentlen = 0;
                /* If there are no longer objects in the list, we expect
                 * the count of reply bytes to be exactly zero. */
                if (listLength(c->reply) == 0)
                    serverAssert(c->reply_bytes == 0);
            }
        }
        /* Note that we avoid to send more than NET_MAX_WRITES_PER_EVENT
         * bytes, in a single threaded server it's a good idea to serve
         * other clients as well, even if a very large request comes from
         * super fast link that is always able to accept data (in real world
         * scenario think about 'KEYS *' against the loopback interface).
         *
         * However if we are over the maxmemory limit we ignore that and
         * just deliver as much data as it is possible to deliver.
         *
         * Moreover, we also send as much as possible if the client is
         * a slave or a monitor (otherwise, on high-speed traffic, the
         * replication/output buffer will grow indefinitely) */
        if (totwritten > NET_MAX_WRITES_PER_EVENT &&
            (server.maxmemory == 0 ||
             zmalloc_used_memory() < server.maxmemory) &&
            !(c->flags & CLIENT_SLAVE))
            break;
    }
    server.stat_net_output_bytes += totwritten;
    if (nwritten == -1) {
        if (errno == EAGAIN) {
            nwritten = 0;
        } else {
            serverLog(LL_VERBOSE,
                      "Error writing to client: %s", strerror(errno));
            freeClient(c);
            return C_ERR;
        }
    }
    if (totwritten > 0) {
        /* For clients representing masters we don't count sending data
         * as an interaction, since we always send REPLCONF ACK commands
         * that take some time to just fill the socket output buffer.
         * We just rely on data / pings received for timeout detection. */
        if (!(c->flags & CLIENT_MASTER)) c->lastinteraction = server.unixtime;
    }
    if (!clientHasPendingReplies(c)) {
        c->sentlen = 0;
        if (handler_installed) aeDeleteFileEvent(server.el, c->fd, AE_WRITABLE);

        /* Close connection after entire reply has been sent. */
        if (c->flags & CLIENT_CLOSE_AFTER_REPLY) {
            freeClient(c);
            return C_ERR;
        }
    }
    return C_OK;
}

/* Write event handler. Just send data to the client. */
void sendReplyToClient(aeEventLoop *el, int fd, void *privdata, int mask) {
    UNUSED(el);
    UNUSED(mask);
    writeToClient(fd, privdata, 1);
}

/*将redis server客户端缓冲区中的数据写回客户端 */
int handleClientsWithPendingWrites(void) {
    listIter li;
    listNode *ln;
    int processed = listLength(server.clients_pending_write);
    //获取待写回的客户端列表
    listRewind(server.clients_pending_write, &li);
    while ((ln = listNext(&li))) {
        client *c = listNodeValue(ln);
        c->flags &= ~CLIENT_PENDING_WRITE;
        listDelNode(server.clients_pending_write, ln);

        /* If a client is protected, don't do anything,
         * that may trigger write error or recreate handler. */
        if (c->flags & CLIENT_PROTECTED) continue;

        /* 调用writeToClient将当前客户端的输出缓冲区数据写回 */
        if (writeToClient(c->fd, c, 0) == C_ERR) continue;

        /* 如果还有待写回数据,说明client回复缓冲区的内容过多,无法一次写到tcp发送缓冲区中 */
        if (clientHasPendingReplies(c)) {
            // 为当前连接注册AE_WRITABLE文件事件回调函数,等待tcp发送缓冲区可写后,继续写入数据.
            int ae_flags = AE_WRITABLE;
            /* 对于 fsync=always 策略，我们希望给定的 FD 永远不会在同一个事件循环迭代中用于读取和写入，
             * 因此在接收查询并将其提供给客户端的过程中，我们将调用 beforeSleep( )，
             * 这将执行 AOF 到磁盘的实际 fsync。 AE_BARRIER 确保了这一点。 */
            if (server.aof_state == AOF_ON &&
                server.aof_fsync == AOF_FSYNC_ALWAYS) {
                ae_flags |= AE_BARRIER;
            }
            // 创建可写事件的监听，以及设置回调函数
            if (aeCreateFileEvent(server.el, c->fd, ae_flags,
                                  sendReplyToClient, c) == AE_ERR) {
                freeClientAsync(c);
            }
        }
    }
    return processed;
}

/* resetClient prepare the client to process the next command */
void resetClient(client *c) {
    redisCommandProc *prevcmd = c->cmd ? c->cmd->proc : NULL;

    freeClientArgv(c);
    c->reqtype = 0;
    c->multibulklen = 0;
    c->bulklen = -1;

    /* We clear the ASKING flag as well if we are not inside a MULTI, and
     * if what we just executed is not the ASKING command itself. */
    if (!(c->flags & CLIENT_MULTI) && prevcmd != askingCommand)
        c->flags &= ~CLIENT_ASKING;

    /* Remove the CLIENT_REPLY_SKIP flag if any so that the reply
     * to the next command will be sent, but set the flag if the command
     * we just processed was "CLIENT REPLY SKIP". */
    c->flags &= ~CLIENT_REPLY_SKIP;
    if (c->flags & CLIENT_REPLY_SKIP_NEXT) {
        c->flags |= CLIENT_REPLY_SKIP;
        c->flags &= ~CLIENT_REPLY_SKIP_NEXT;
    }
}

/* This funciton is used when we want to re-enter the event loop but there
 * is the risk that the client we are dealing with will be freed in some
 * way. This happens for instance in:
 *
 * * DEBUG RELOAD and similar.
 * * When a Lua script is in -BUSY state.
 *
 * So the function will protect the client by doing two things:
 *
 * 1) It removes the file events. This way it is not possible that an
 *    error is signaled on the socket, freeing the client.
 * 2) Moreover it makes sure that if the client is freed in a different code
 *    path, it is not really released, but only marked for later release. */
void protectClient(client *c) {
    c->flags |= CLIENT_PROTECTED;
    aeDeleteFileEvent(server.el, c->fd, AE_READABLE);
    aeDeleteFileEvent(server.el, c->fd, AE_WRITABLE);
}

/* This will undo the client protection done by protectClient() */
void unprotectClient(client *c) {
    if (c->flags & CLIENT_PROTECTED) {
        c->flags &= ~CLIENT_PROTECTED;
        aeCreateFileEvent(server.el, c->fd, AE_READABLE, readQueryFromClient, c);
        if (clientHasPendingReplies(c)) clientInstallWriteHandler(c);
    }
}

/* Like processMultibulkBuffer(), but for the inline protocol instead of RESP,
 * this function consumes the client query buffer and creates a command ready
 * to be executed inside the client structure. Returns C_OK if the command
 * is ready to be executed, or C_ERR if there is still protocol to read to
 * have a well formed command. The function also returns C_ERR when there is
 * a protocol error: in such a case the client structure is setup to reply
 * with the error and close the connection. */
int processInlineBuffer(client *c) {
    char *newline;
    int argc, j, linefeed_chars = 1;
    sds *argv, aux;
    size_t querylen;

    /* Search for end of line */
    newline = strchr(c->querybuf + c->qb_pos, '\n');

    /* Nothing to do without a \r\n */
    if (newline == NULL) {
        if (sdslen(c->querybuf) - c->qb_pos > PROTO_INLINE_MAX_SIZE) {
            addReplyError(c, "Protocol error: too big inline request");
            setProtocolError("too big inline request", c);
        }
        return C_ERR;
    }

    /* Handle the \r\n case. */
    if (newline && newline != c->querybuf + c->qb_pos && *(newline - 1) == '\r')
        newline--, linefeed_chars++;

    /* Split the input buffer up to the \r\n */
    querylen = newline - (c->querybuf + c->qb_pos);
    aux = sdsnewlen(c->querybuf + c->qb_pos, querylen);
    argv = sdssplitargs(aux, &argc);
    sdsfree(aux);
    if (argv == NULL) {
        addReplyError(c, "Protocol error: unbalanced quotes in request");
        setProtocolError("unbalanced quotes in inline request", c);
        return C_ERR;
    }

    /* Newline from slaves can be used to refresh the last ACK time.
     * This is useful for a slave to ping back while loading a big
     * RDB file. */
    if (querylen == 0 && getClientType(c) == CLIENT_TYPE_SLAVE)
        c->repl_ack_time = server.unixtime;

    /* Move querybuffer position to the next query in the buffer. */
    c->qb_pos += querylen + linefeed_chars;

    /* Setup argv array on client structure */
    if (argc) {
        if (c->argv) zfree(c->argv);
        c->argv = zmalloc(sizeof(robj *) * argc);
    }

    /* Create redis objects for all arguments. */
    for (c->argc = 0, j = 0; j < argc; j++) {
        c->argv[c->argc] = createObject(OBJ_STRING, argv[j]);
        c->argc++;
    }
    zfree(argv);
    return C_OK;
}

/* Helper function. Record protocol erro details in server log,
 * and set the client as CLIENT_CLOSE_AFTER_REPLY. */
#define PROTO_DUMP_LEN 128

static void setProtocolError(const char *errstr, client *c) {
    if (server.verbosity <= LL_VERBOSE) {
        sds client = catClientInfoString(sdsempty(), c);

        /* Sample some protocol to given an idea about what was inside. */
        char buf[256];
        if (sdslen(c->querybuf) - c->qb_pos < PROTO_DUMP_LEN) {
            snprintf(buf, sizeof(buf), "Query buffer during protocol error: '%s'", c->querybuf + c->qb_pos);
        } else {
            snprintf(buf, sizeof(buf), "Query buffer during protocol error: '%.*s' (... more %zu bytes ...) '%.*s'",
                     PROTO_DUMP_LEN / 2, c->querybuf + c->qb_pos, sdslen(c->querybuf) - c->qb_pos - PROTO_DUMP_LEN,
                     PROTO_DUMP_LEN / 2, c->querybuf + sdslen(c->querybuf) - PROTO_DUMP_LEN / 2);
        }

        /* Remove non printable chars. */
        char *p = buf;
        while (*p != '\0') {
            if (!isprint(*p)) *p = '.';
            p++;
        }

        /* Log all the client and protocol info. */
        serverLog(LL_VERBOSE,
                  "Protocol error (%s) from client: %s. %s", errstr, client, buf);
        sdsfree(client);
    }
    c->flags |= CLIENT_CLOSE_AFTER_REPLY;
}

/* 从查询缓冲区的数据中解析请求报文,获取命令名及命令参数 */
int processMultibulkBuffer(client *c) {
    char *newline = NULL;
    int ok;
    long long ll;
    // c->multibulklen == 0代表上一个命令请求数据已解析完全,这里开始解析一个新的命令请求.
    if (c->multibulklen == 0) {
        serverAssertWithInfo(c, NULL, c->argc == 0);

        /* *3\r\n$3\r\nset\r\n$4\r\ntian\r\n$3\r\n666\r\n ---> \r\n$3\r\nset\r\n$4\r\ntian\r\n$3\r\n666\r\n */
        newline = strchr(c->querybuf + c->qb_pos, '\r');
        if (newline == NULL) {
            if (sdslen(c->querybuf) - c->qb_pos > PROTO_INLINE_MAX_SIZE) {
                addReplyError(c, "Protocol error: too big mbulk count string");
                setProtocolError("too big mbulk count string", c);
            }
            return C_ERR;
        }

        /* Buffer should also contain \n */
        if (newline - (c->querybuf + c->qb_pos) > (ssize_t) (sdslen(c->querybuf) - c->qb_pos - 2))
            return C_ERR;

        /* We know for sure there is a whole line since newline != NULL,
         * so go ahead and find out the multi bulk length. */
        serverAssertWithInfo(c, NULL, c->querybuf[c->qb_pos] == '*');
        ok = string2ll(c->querybuf + 1 + c->qb_pos, newline - (c->querybuf + 1 + c->qb_pos), &ll);  // 找出命令的行数,赋值给ll
        if (!ok || ll > 1024 * 1024) {
            addReplyError(c, "Protocol error: invalid multibulk length");
            setProtocolError("invalid mbulk count", c);
            return C_ERR;
        } else if (ll > 10 && server.requirepass && !c->authenticated) {
            addReplyError(c, "Protocol error: unauthenticated multibulk length");
            setProtocolError("unauth mbulk count", c);
            return C_ERR;
        }
        // c->qb_pos指向$
        c->qb_pos = (newline - c->querybuf) + 2;

        if (ll <= 0) return C_OK;

        c->multibulklen = ll;

        /* Setup argv array on client structure */
        if (c->argv) zfree(c->argv);
        c->argv = zmalloc(sizeof(robj *) * c->multibulklen);
    }
    serverAssertWithInfo(c, NULL, c->multibulklen > 0);
    // 读取当前命令的所有参数
    while (c->multibulklen) {
        if (c->bulklen == -1) {
            // 通过\r\n分隔符读取当前参数长度,赋值给c->bulklen
            newline = strchr(c->querybuf + c->qb_pos, '\r');
            if (newline == NULL) {
                if (sdslen(c->querybuf) - c->qb_pos > PROTO_INLINE_MAX_SIZE) {
                    addReplyError(c,
                                  "Protocol error: too big bulk count string");
                    setProtocolError("too big bulk count string", c);
                    return C_ERR;
                }
                break;
            }

            /* Buffer should also contain \n */
            if (newline - (c->querybuf + c->qb_pos) > (ssize_t) (sdslen(c->querybuf) - c->qb_pos - 2))
                break;

            if (c->querybuf[c->qb_pos] != '$') {
                addReplyErrorFormat(c,
                                    "Protocol error: expected '$', got '%c'",
                                    c->querybuf[c->qb_pos]);
                setProtocolError("expected $ but got something else", c);
                return C_ERR;
            }

            ok = string2ll(c->querybuf + c->qb_pos + 1, newline - (c->querybuf + c->qb_pos + 1), &ll);
            if (!ok || ll < 0 || ll > server.proto_max_bulk_len) {
                addReplyError(c, "Protocol error: invalid bulk length");
                setProtocolError("invalid bulk length", c);
                return C_ERR;
            } else if (ll > 16384 && server.requirepass && !c->authenticated) {
                addReplyError(c, "Protocol error: unauthenticated bulk length");
                setProtocolError("unauth bulk length", c);
                return C_ERR;
            }

            c->qb_pos = newline - c->querybuf + 2;
            /* 如果当前参数是一个超大参数,则执行以下优化:
             * 清除查询缓冲区中其他参数的数据(这些参数已处理),确保查询缓冲区只有当前参数数据,并对缓冲区扩容,
             * 确保可以容纳当前参数.
             * */
            if (ll >= PROTO_MBULK_BIG_ARG) {
                if (sdslen(c->querybuf) - c->qb_pos <= (size_t) ll + 2) {
                    sdsrange(c->querybuf, c->qb_pos, -1);
                    c->qb_pos = 0;
                    /* Hint the sds library about the amount of bytes this string is
                     * going to contain. */
                    c->querybuf = sdsMakeRoomFor(c->querybuf, ll + 2);
                }
            }
            c->bulklen = ll;
        }

        /* 当前查询缓冲区字符串长度小于当前参数长度,说明当前参数没有读取完整,退出函数 */
        if (sdslen(c->querybuf) - c->qb_pos < (size_t) (c->bulklen + 2)) {
            /* Not enough data (+2 == trailing \r\n) */
            break;
        } else {
            /* 如果读取的是超大参数,则直接使用查询缓冲区创建一个robj作为参数,
             * 并申请新的内存作为查询缓冲区
             * */
            if (c->qb_pos == 0 &&
                c->bulklen >= PROTO_MBULK_BIG_ARG &&
                sdslen(c->querybuf) == (size_t) (c->bulklen + 2)) {

                c->argv[c->argc++] = createObject(OBJ_STRING, c->querybuf);
                sdsIncrLen(c->querybuf, -2); /* remove CRLF */
                c->querybuf = sdsnewlen(SDS_NOINIT, c->bulklen + 2);
                sdsclear(c->querybuf);
            } else {
                // 如果读取的非超大参数,则调用createStringObject函数复制查询缓冲区中的数据
                // 并创建一个robj对象.
                c->argv[c->argc++] = createStringObject(c->querybuf + c->qb_pos, c->bulklen);
                c->qb_pos += c->bulklen + 2;
            }
            c->bulklen = -1;
            c->multibulklen--;
        }
    }

    /* c->multibulklen == 0代表当前命令数据已读取完全 */
    if (c->multibulklen == 0) return C_OK;

    /* Still not ready to process the command */
    return C_ERR;
}

/* 处理输入缓冲区 */
void processInputBuffer(client *c) {
    // 设置当前客户端
    server.current_client = c;

    // 持续处理缓冲区数据
    while (c->qb_pos < sdslen(c->querybuf)) {
        // 客户端被暂停,跳出循环
        if (!(c->flags & CLIENT_SLAVE) && clientsArePaused()) break;

        // 客户端正忙,跳出循环
        if (c->flags & CLIENT_BLOCKED) break;

        // 主服务器有脚本正在执行,仅积累命令
        if (server.lua_timedout && c->flags & CLIENT_MASTER) break;

        // 要关闭连接的客户端,跳出循环
        if (c->flags & (CLIENT_CLOSE_AFTER_REPLY | CLIENT_CLOSE_ASAP)) break;

        // 请求数据类型未确认,代表当前解析的是一个新命令请求,因此需要判断请求的数据类型.
        if (!c->reqtype) {
            // *开头
            if (c->querybuf[c->qb_pos] == '*') {
                c->reqtype = PROTO_REQ_MULTIBULK;
            } else {
                c->reqtype = PROTO_REQ_INLINE;
            }
        }
        // 处理不同类型请求
        if (c->reqtype == PROTO_REQ_INLINE) {
            if (processInlineBuffer(c) != C_OK) break;
        } else if (c->reqtype == PROTO_REQ_MULTIBULK) {
            if (processMultibulkBuffer(c) != C_OK) break;
        } else {
            serverPanic("Unknown request type");
        }

        /* Multibulk processing could see a <= 0 length. */
        if (c->argc == 0) {
            resetClient(c);
        } else {
            /* 执行命令 */
            if (processCommand(c) == C_OK) {
                if (c->flags & CLIENT_MASTER && !(c->flags & CLIENT_MULTI)) {
                    /* Update the applied replication offset of our master. */
                    c->reploff = c->read_reploff - sdslen(c->querybuf) + c->qb_pos;
                }

                // 重设客户端状态
                if (!(c->flags & CLIENT_BLOCKED) || c->btype != BLOCKED_MODULE)
                    resetClient(c);
            }
            // 跳过已释放客户端
            if (server.current_client == NULL) break;
        }
    }

    /* 到这里,说明命令执行成功,抛弃查询缓冲区中已处理的命令请求报文,并赋值qb_pos为0 */
    if (server.current_client != NULL && c->qb_pos) {
        sdsrange(c->querybuf, c->qb_pos, -1);
        c->qb_pos = 0;
    }
    // 重置当前客户端
    server.current_client = NULL;
}

/* 在处理输入缓冲区的同时确保主从复制的正确进行 */
void processInputBufferAndReplicate(client *c) {
    if (!(c->flags & CLIENT_MASTER)) {
        processInputBuffer(c);
    } else {
        // 处理输入缓冲区前的偏移量
        size_t prev_offset = c->reploff;
        processInputBuffer(c);
        // 计算已应用的复制偏移量
        size_t applied = c->reploff - prev_offset;
        // 如果有应用的复制偏移量
        if (applied) {
            // 从主服务器流中复制到从服务器
            replicationFeedSlavesFromMasterStream(server.slaves,
                                                  c->pending_querybuf, applied);
            // 移除已应用的部分
            sdsrange(c->pending_querybuf, applied, -1);
        }
    }
}

/* RESP 协议的数据类型包括：
 * 简单字符串（Simple String）：以 “+” 字符开头，例如：“+OK\r\n”
 * 错误字符串（Error String）：以 “-” 字符开头，例如：“-Error message\r\n”
 * 整数（Integer）：以 “:” 字符开头，例如：“:1000\r\n”
 * 批量字符串（Bulk String）：以 “$” 字符开头，例如：“$5\r\nhello\r\n”
 * 数组（Array）：以 “*” 字符开头，例如：“*3\r\n$5\r\nhello\r\n$5\r\nworld\r\n:1000\r\n”
 * */
void readQueryFromClient(aeEventLoop *el, int fd, void *privdata, int mask) {
    client *c = (client *) privdata;
    int nread, readlen;
    size_t qblen;
    UNUSED(el); //避免无用参数警告
    UNUSED(mask);
    // 读取请求最大字节数,默认16KB
    readlen = PROTO_IOBUF_LEN;
    /* 如果当前读取的是超大参数(长度大于PROTO_MBULK_BIG_ARG),则需要保证查询缓冲区中只有当前参数数据.
     * c->multibulklen不为0.代表发生了TCP拆包,readQueryFromClient上一次并没有完整读取命令请求(
     * 读取完整的命令请求会将该属性重置为0).
     * */
    if (c->reqtype == PROTO_REQ_MULTIBULK && c->multibulklen && c->bulklen != -1
        && c->bulklen >= PROTO_MBULK_BIG_ARG) {
        ssize_t remaining = (size_t) (c->bulklen + 2) - sdslen(c->querybuf);

        /* 如果这时读取的是超大参数,并且该参数剩余字节数小于readlen,则只读取当前参数剩余字节数,从而
         * 保证缓冲区中只有当前参数数据.
         * */
        if (remaining > 0 && remaining < readlen) readlen = remaining;
    }
    // 计算已有查询缓冲数据大小
    qblen = sdslen(c->querybuf);
    // 更新峰值记录
    if (c->querybuf_peak < qblen) c->querybuf_peak = qblen;
    // 扩容查询缓冲区,保证可用内存不小于读取字节数readlen
    c->querybuf = sdsMakeRoomFor(c->querybuf, readlen);
    // 从socket读取到缓冲区
    nread = read(fd, c->querybuf + qblen, readlen);
    if (nread == -1) {
        if (errno == EAGAIN) {
            return;
        } else {
            serverLog(LL_VERBOSE, "Reading from client: %s", strerror(errno));
            freeClient(c);
            return;
        }
    } else if (nread == 0) {
        serverLog(LL_VERBOSE, "Client closed connection");
        freeClient(c);
        return;
    } else if (c->flags & CLIENT_MASTER) {
        /* Append the query buffer to the pending (not applied) buffer
         * of the master. We'll use this buffer later in order to have a
         * copy of the string applied by the last command executed. */
        c->pending_querybuf = sdscatlen(c->pending_querybuf,
                                        c->querybuf + qblen, nread);
    }
    // 更新状态
    sdsIncrLen(c->querybuf, nread);
    c->lastinteraction = server.unixtime;
    if (c->flags & CLIENT_MASTER) c->read_reploff += nread;
    server.stat_net_input_bytes += nread;
    if (sdslen(c->querybuf) > server.client_max_querybuf_len) {
        sds ci = catClientInfoString(sdsempty(), c), bytes = sdsempty();

        bytes = sdscatrepr(bytes, c->querybuf, 64);
        serverLog(LL_WARNING, "Closing client that reached max query buffer length: %s (qbuf initial bytes: %s)", ci,
                  bytes);
        sdsfree(ci);
        sdsfree(bytes);
        freeClient(c);
        return;
    }

    /* 处理缓冲区的时间。 如果客户端是主服务器，
     * 我们需要计算处理缓冲区之前和之后应用的偏移量之间的差异，
     * 以了解有多少复制流实际应用于主状态：该数量及其复制流的相应部分 ，
     * 将被传播到slave和复制积压缓冲区。
     * */
    processInputBufferAndReplicate(c);
}

void getClientsMaxBuffers(unsigned long *longest_output_list,
                          unsigned long *biggest_input_buffer) {
    client *c;
    listNode *ln;
    listIter li;
    unsigned long lol = 0, bib = 0;

    listRewind(server.clients, &li);
    while ((ln = listNext(&li)) != NULL) {
        c = listNodeValue(ln);

        if (listLength(c->reply) > lol) lol = listLength(c->reply);
        if (sdslen(c->querybuf) > bib) bib = sdslen(c->querybuf);
    }
    *longest_output_list = lol;
    *biggest_input_buffer = bib;
}

/* A Redis "Peer ID" is a colon separated ip:port pair.
 * For IPv4 it's in the form x.y.z.k:port, example: "127.0.0.1:1234".
 * For IPv6 addresses we use [] around the IP part, like in "[::1]:1234".
 * For Unix sockets we use path:0, like in "/tmp/redis:0".
 *
 * A Peer ID always fits inside a buffer of NET_PEER_ID_LEN bytes, including
 * the null term.
 *
 * On failure the function still populates 'peerid' with the "?:0" string
 * in case you want to relax error checking or need to display something
 * anyway (see anetPeerToString implementation for more info). */
void genClientPeerId(client *client, char *peerid,
                     size_t peerid_len) {
    if (client->flags & CLIENT_UNIX_SOCKET) {
        /* Unix socket client. */
        snprintf(peerid, peerid_len, "%s:0", server.unixsocket);
    } else {
        /* TCP client. */
        anetFormatPeer(client->fd, peerid, peerid_len);
    }
}

/* This function returns the client peer id, by creating and caching it
 * if client->peerid is NULL, otherwise returning the cached value.
 * The Peer ID never changes during the life of the client, however it
 * is expensive to compute. */
char *getClientPeerId(client *c) {
    char peerid[NET_PEER_ID_LEN];

    if (c->peerid == NULL) {
        genClientPeerId(c, peerid, sizeof(peerid));
        c->peerid = sdsnew(peerid);
    }
    return c->peerid;
}

/* Concatenate a string representing the state of a client in an human
 * readable format, into the sds string 's'. */
sds catClientInfoString(sds s, client *client) {
    char flags[16], events[3], *p;
    int emask;

    p = flags;
    if (client->flags & CLIENT_SLAVE) {
        if (client->flags & CLIENT_MONITOR)
            *p++ = 'O';
        else
            *p++ = 'S';
    }
    if (client->flags & CLIENT_MASTER) *p++ = 'M';
    if (client->flags & CLIENT_PUBSUB) *p++ = 'P';
    if (client->flags & CLIENT_MULTI) *p++ = 'x';
    if (client->flags & CLIENT_BLOCKED) *p++ = 'b';
    if (client->flags & CLIENT_DIRTY_CAS) *p++ = 'd';
    if (client->flags & CLIENT_CLOSE_AFTER_REPLY) *p++ = 'c';
    if (client->flags & CLIENT_UNBLOCKED) *p++ = 'u';
    if (client->flags & CLIENT_CLOSE_ASAP) *p++ = 'A';
    if (client->flags & CLIENT_UNIX_SOCKET) *p++ = 'U';
    if (client->flags & CLIENT_READONLY) *p++ = 'r';
    if (p == flags) *p++ = 'N';
    *p++ = '\0';

    emask = client->fd == -1 ? 0 : aeGetFileEvents(server.el, client->fd);
    p = events;
    if (emask & AE_READABLE) *p++ = 'r';
    if (emask & AE_WRITABLE) *p++ = 'w';
    *p = '\0';
    return sdscatfmt(s,
                     "id=%U addr=%s fd=%i name=%s age=%I idle=%I flags=%s db=%i sub=%i psub=%i multi=%i qbuf=%U qbuf-free=%U obl=%U oll=%U omem=%U events=%s cmd=%s",
                     (unsigned long long) client->id,
                     getClientPeerId(client),
                     client->fd,
                     client->name ? (char *) client->name->ptr : "",
                     (long long) (server.unixtime - client->ctime),
                     (long long) (server.unixtime - client->lastinteraction),
                     flags,
                     client->db->id,
                     (int) dictSize(client->pubsub_channels),
                     (int) listLength(client->pubsub_patterns),
                     (client->flags & CLIENT_MULTI) ? client->mstate.count : -1,
                     (unsigned long long) sdslen(client->querybuf),
                     (unsigned long long) sdsavail(client->querybuf),
                     (unsigned long long) client->bufpos,
                     (unsigned long long) listLength(client->reply),
                     (unsigned long long) getClientOutputBufferMemoryUsage(client),
                     events,
                     client->lastcmd ? client->lastcmd->name : "NULL");
}

sds getAllClientsInfoString(int type) {
    listNode *ln;
    listIter li;
    client *client;
    sds o = sdsnewlen(SDS_NOINIT, 200 * listLength(server.clients));
    sdsclear(o);
    listRewind(server.clients, &li);
    while ((ln = listNext(&li)) != NULL) {
        client = listNodeValue(ln);
        if (type != -1 && getClientType(client) != type) continue;
        o = catClientInfoString(o, client);
        o = sdscatlen(o, "\n", 1);
    }
    return o;
}

void clientCommand(client *c) {
    listNode *ln;
    listIter li;
    client *client;

    if (c->argc == 2 && !strcasecmp(c->argv[1]->ptr, "help")) {
        const char *help[] = {
                "id                     -- Return the ID of the current connection.",
                "getname                -- Return the name of the current connection.",
                "kill <ip:port>         -- Kill connection made from <ip:port>.",
                "kill <option> <value> [option value ...] -- Kill connections. Options are:",
                "     addr <ip:port>                      -- Kill connection made from <ip:port>",
                "     type (normal|master|replica|pubsub) -- Kill connections by type.",
                "     skipme (yes|no)   -- Skip killing current connection (default: yes).",
                "list [options ...]     -- Return information about client connections. Options:",
                "     type (normal|master|replica|pubsub) -- Return clients of specified type.",
                "pause <timeout>        -- Suspend all Redis clients for <timout> milliseconds.",
                "reply (on|off|skip)    -- Control the replies sent to the current connection.",
                "setname <name>         -- Assign the name <name> to the current connection.",
                "unblock <clientid> [TIMEOUT|ERROR] -- Unblock the specified blocked client.",
                NULL
        };
        addReplyHelp(c, help);
    } else if (!strcasecmp(c->argv[1]->ptr, "id") && c->argc == 2) {
        /* CLIENT ID */
        addReplyLongLong(c, c->id);
    } else if (!strcasecmp(c->argv[1]->ptr, "list")) {
        /* CLIENT LIST */
        int type = -1;
        if (c->argc == 4 && !strcasecmp(c->argv[2]->ptr, "type")) {
            type = getClientTypeByName(c->argv[3]->ptr);
            if (type == -1) {
                addReplyErrorFormat(c, "Unknown client type '%s'",
                                    (char *) c->argv[3]->ptr);
                return;
            }
        } else if (c->argc != 2) {
            addReply(c, shared.syntaxerr);
            return;
        }
        sds o = getAllClientsInfoString(type);
        addReplyBulkCBuffer(c, o, sdslen(o));
        sdsfree(o);
    } else if (!strcasecmp(c->argv[1]->ptr, "reply") && c->argc == 3) {
        /* CLIENT REPLY ON|OFF|SKIP */
        if (!strcasecmp(c->argv[2]->ptr, "on")) {
            c->flags &= ~(CLIENT_REPLY_SKIP | CLIENT_REPLY_OFF);
            addReply(c, shared.ok);
        } else if (!strcasecmp(c->argv[2]->ptr, "off")) {
            c->flags |= CLIENT_REPLY_OFF;
        } else if (!strcasecmp(c->argv[2]->ptr, "skip")) {
            if (!(c->flags & CLIENT_REPLY_OFF))
                c->flags |= CLIENT_REPLY_SKIP_NEXT;
        } else {
            addReply(c, shared.syntaxerr);
            return;
        }
    } else if (!strcasecmp(c->argv[1]->ptr, "kill")) {
        /* CLIENT KILL <ip:port>
         * CLIENT KILL <option> [value] ... <option> [value] */
        char *addr = NULL;
        int type = -1;
        uint64_t id = 0;
        int skipme = 1;
        int killed = 0, close_this_client = 0;

        if (c->argc == 3) {
            /* Old style syntax: CLIENT KILL <addr> */
            addr = c->argv[2]->ptr;
            skipme = 0; /* With the old form, you can kill yourself. */
        } else if (c->argc > 3) {
            int i = 2; /* Next option index. */

            /* New style syntax: parse options. */
            while (i < c->argc) {
                int moreargs = c->argc > i + 1;

                if (!strcasecmp(c->argv[i]->ptr, "id") && moreargs) {
                    long long tmp;

                    if (getLongLongFromObjectOrReply(c, c->argv[i + 1], &tmp, NULL)
                        != C_OK)
                        return;
                    id = tmp;
                } else if (!strcasecmp(c->argv[i]->ptr, "type") && moreargs) {
                    type = getClientTypeByName(c->argv[i + 1]->ptr);
                    if (type == -1) {
                        addReplyErrorFormat(c, "Unknown client type '%s'",
                                            (char *) c->argv[i + 1]->ptr);
                        return;
                    }
                } else if (!strcasecmp(c->argv[i]->ptr, "addr") && moreargs) {
                    addr = c->argv[i + 1]->ptr;
                } else if (!strcasecmp(c->argv[i]->ptr, "skipme") && moreargs) {
                    if (!strcasecmp(c->argv[i + 1]->ptr, "yes")) {
                        skipme = 1;
                    } else if (!strcasecmp(c->argv[i + 1]->ptr, "no")) {
                        skipme = 0;
                    } else {
                        addReply(c, shared.syntaxerr);
                        return;
                    }
                } else {
                    addReply(c, shared.syntaxerr);
                    return;
                }
                i += 2;
            }
        } else {
            addReply(c, shared.syntaxerr);
            return;
        }

        /* Iterate clients killing all the matching clients. */
        listRewind(server.clients, &li);
        while ((ln = listNext(&li)) != NULL) {
            client = listNodeValue(ln);
            if (addr && strcmp(getClientPeerId(client), addr) != 0) continue;
            if (type != -1 && getClientType(client) != type) continue;
            if (id != 0 && client->id != id) continue;
            if (c == client && skipme) continue;

            /* Kill it. */
            if (c == client) {
                close_this_client = 1;
            } else {
                freeClient(client);
            }
            killed++;
        }

        /* Reply according to old/new format. */
        if (c->argc == 3) {
            if (killed == 0)
                addReplyError(c, "No such client");
            else
                addReply(c, shared.ok);
        } else {
            addReplyLongLong(c, killed);
        }

        /* If this client has to be closed, flag it as CLOSE_AFTER_REPLY
         * only after we queued the reply to its output buffers. */
        if (close_this_client) c->flags |= CLIENT_CLOSE_AFTER_REPLY;
    } else if (!strcasecmp(c->argv[1]->ptr, "unblock") && (c->argc == 3 ||
                                                           c->argc == 4)) {
        /* CLIENT UNBLOCK <id> [timeout|error] */
        long long id;
        int unblock_error = 0;

        if (c->argc == 4) {
            if (!strcasecmp(c->argv[3]->ptr, "timeout")) {
                unblock_error = 0;
            } else if (!strcasecmp(c->argv[3]->ptr, "error")) {
                unblock_error = 1;
            } else {
                addReplyError(c,
                              "CLIENT UNBLOCK reason should be TIMEOUT or ERROR");
                return;
            }
        }
        if (getLongLongFromObjectOrReply(c, c->argv[2], &id, NULL)
            != C_OK)
            return;
        struct client *target = lookupClientByID(id);
        if (target && target->flags & CLIENT_BLOCKED) {
            if (unblock_error)
                addReplyError(target,
                              "-UNBLOCKED client unblocked via CLIENT UNBLOCK");
            else
                replyToBlockedClientTimedOut(target);
            unblockClient(target);
            addReply(c, shared.cone);
        } else {
            addReply(c, shared.czero);
        }
    } else if (!strcasecmp(c->argv[1]->ptr, "setname") && c->argc == 3) {
        int j, len = sdslen(c->argv[2]->ptr);
        char *p = c->argv[2]->ptr;

        /* Setting the client name to an empty string actually removes
         * the current name. */
        if (len == 0) {
            if (c->name) decrRefCount(c->name);
            c->name = NULL;
            addReply(c, shared.ok);
            return;
        }

        /* Otherwise check if the charset is ok. We need to do this otherwise
         * CLIENT LIST format will break. You should always be able to
         * split by space to get the different fields. */
        for (j = 0; j < len; j++) {
            if (p[j] < '!' || p[j] > '~') { /* ASCII is assumed. */
                addReplyError(c,
                              "Client names cannot contain spaces, "
                              "newlines or special characters.");
                return;
            }
        }
        if (c->name) decrRefCount(c->name);
        c->name = c->argv[2];
        incrRefCount(c->name);
        addReply(c, shared.ok);
    } else if (!strcasecmp(c->argv[1]->ptr, "getname") && c->argc == 2) {
        if (c->name)
            addReplyBulk(c, c->name);
        else
            addReply(c, shared.nullbulk);
    } else if (!strcasecmp(c->argv[1]->ptr, "pause") && c->argc == 3) {
        long long duration;

        if (getTimeoutFromObjectOrReply(c, c->argv[2], &duration, UNIT_MILLISECONDS)
            != C_OK)
            return;
        pauseClients(duration);
        addReply(c, shared.ok);
    } else {
        addReplyErrorFormat(c, "Unknown subcommand or wrong number of arguments for '%s'. Try CLIENT HELP",
                            (char *) c->argv[1]->ptr);
    }
}

/* This callback is bound to POST and "Host:" command names. Those are not
 * really commands, but are used in security attacks in order to talk to
 * Redis instances via HTTP, with a technique called "cross protocol scripting"
 * which exploits the fact that services like Redis will discard invalid
 * HTTP headers and will process what follows.
 *
 * As a protection against this attack, Redis will terminate the connection
 * when a POST or "Host:" header is seen, and will log the event from
 * time to time (to avoid creating a DOS as a result of too many logs). */
void securityWarningCommand(client *c) {
    static time_t logged_time;
    time_t now = time(NULL);

    if (labs(now - logged_time) > 60) {
        serverLog(LL_WARNING,
                  "Possible SECURITY ATTACK detected. It looks like somebody is sending POST or Host: commands to Redis. This is likely due to an attacker attempting to use Cross Protocol Scripting to compromise your Redis instance. Connection aborted.");
        logged_time = now;
    }
    freeClientAsync(c);
}

/* Rewrite the command vector of the client. All the new objects ref count
 * is incremented. The old command vector is freed, and the old objects
 * ref count is decremented. */
void rewriteClientCommandVector(client *c, int argc, ...) {
    va_list ap;
    int j;
    robj **argv; /* The new argument vector */

    argv = zmalloc(sizeof(robj *) * argc);
    va_start(ap, argc);
    for (j = 0; j < argc; j++) {
        robj *a;

        a = va_arg(ap, robj*);
        argv[j] = a;
        incrRefCount(a);
    }
    /* We free the objects in the original vector at the end, so we are
     * sure that if the same objects are reused in the new vector the
     * refcount gets incremented before it gets decremented. */
    for (j = 0; j < c->argc; j++) decrRefCount(c->argv[j]);
    zfree(c->argv);
    /* Replace argv and argc with our new versions. */
    c->argv = argv;
    c->argc = argc;
    c->cmd = lookupCommandOrOriginal(c->argv[0]->ptr);
    serverAssertWithInfo(c, NULL, c->cmd != NULL);
    va_end(ap);
}

/* Completely replace the client command vector with the provided one. */
void replaceClientCommandVector(client *c, int argc, robj **argv) {
    freeClientArgv(c);
    zfree(c->argv);
    c->argv = argv;
    c->argc = argc;
    c->cmd = lookupCommandOrOriginal(c->argv[0]->ptr);
    serverAssertWithInfo(c, NULL, c->cmd != NULL);
}

/* Rewrite a single item in the command vector.
 * The new val ref count is incremented, and the old decremented.
 *
 * It is possible to specify an argument over the current size of the
 * argument vector: in this case the array of objects gets reallocated
 * and c->argc set to the max value. However it's up to the caller to
 *
 * 1. Make sure there are no "holes" and all the arguments are set.
 * 2. If the original argument vector was longer than the one we
 *    want to end with, it's up to the caller to set c->argc and
 *    free the no longer used objects on c->argv. */
void rewriteClientCommandArgument(client *c, int i, robj *newval) {
    robj *oldval;

    if (i >= c->argc) {
        c->argv = zrealloc(c->argv, sizeof(robj *) * (i + 1));
        c->argc = i + 1;
        c->argv[i] = NULL;
    }
    oldval = c->argv[i];
    c->argv[i] = newval;
    incrRefCount(newval);
    if (oldval) decrRefCount(oldval);

    /* If this is the command name make sure to fix c->cmd. */
    if (i == 0) {
        c->cmd = lookupCommandOrOriginal(c->argv[0]->ptr);
        serverAssertWithInfo(c, NULL, c->cmd != NULL);
    }
}

/* This function returns the number of bytes that Redis is
 * using to store the reply still not read by the client.
 *
 * Note: this function is very fast so can be called as many time as
 * the caller wishes. The main usage of this function currently is
 * enforcing the client output length limits. */
unsigned long getClientOutputBufferMemoryUsage(client *c) {
    unsigned long list_item_size = sizeof(listNode) + sizeof(clientReplyBlock);
    return c->reply_bytes + (list_item_size * listLength(c->reply));
}

/* Get the class of a client, used in order to enforce limits to different
 * classes of clients.
 *
 * The function will return one of the following:
 * CLIENT_TYPE_NORMAL -> Normal client
 * CLIENT_TYPE_SLAVE  -> Slave
 * CLIENT_TYPE_PUBSUB -> Client subscribed to Pub/Sub channels
 * CLIENT_TYPE_MASTER -> The client representing our replication master.
 */
int getClientType(client *c) {
    if (c->flags & CLIENT_MASTER) return CLIENT_TYPE_MASTER;
    /* Even though MONITOR clients are marked as replicas, we
     * want the expose them as normal clients. */
    if ((c->flags & CLIENT_SLAVE) && !(c->flags & CLIENT_MONITOR))
        return CLIENT_TYPE_SLAVE;
    if (c->flags & CLIENT_PUBSUB) return CLIENT_TYPE_PUBSUB;
    return CLIENT_TYPE_NORMAL;
}

int getClientTypeByName(char *name) {
    if (!strcasecmp(name, "normal")) return CLIENT_TYPE_NORMAL;
    else if (!strcasecmp(name, "slave")) return CLIENT_TYPE_SLAVE;
    else if (!strcasecmp(name, "replica")) return CLIENT_TYPE_SLAVE;
    else if (!strcasecmp(name, "pubsub")) return CLIENT_TYPE_PUBSUB;
    else if (!strcasecmp(name, "master")) return CLIENT_TYPE_MASTER;
    else return -1;
}

char *getClientTypeName(int class) {
    switch (class) {
        case CLIENT_TYPE_NORMAL:
            return "normal";
        case CLIENT_TYPE_SLAVE:
            return "slave";
        case CLIENT_TYPE_PUBSUB:
            return "pubsub";
        case CLIENT_TYPE_MASTER:
            return "master";
        default:
            return NULL;
    }
}

/* The function checks if the client reached output buffer soft or hard
 * limit, and also update the state needed to check the soft limit as
 * a side effect.
 *
 * Return value: non-zero if the client reached the soft or the hard limit.
 *               Otherwise zero is returned. */
int checkClientOutputBufferLimits(client *c) {
    int soft = 0, hard = 0, class;
    unsigned long used_mem = getClientOutputBufferMemoryUsage(c);

    class = getClientType(c);
    /* For the purpose of output buffer limiting, masters are handled
     * like normal clients. */
    if (class == CLIENT_TYPE_MASTER) class = CLIENT_TYPE_NORMAL;

    if (server.client_obuf_limits[class].hard_limit_bytes &&
        used_mem >= server.client_obuf_limits[class].hard_limit_bytes)
        hard = 1;
    if (server.client_obuf_limits[class].soft_limit_bytes &&
        used_mem >= server.client_obuf_limits[class].soft_limit_bytes)
        soft = 1;

    /* We need to check if the soft limit is reached continuously for the
     * specified amount of seconds. */
    if (soft) {
        if (c->obuf_soft_limit_reached_time == 0) {
            c->obuf_soft_limit_reached_time = server.unixtime;
            soft = 0; /* First time we see the soft limit reached */
        } else {
            time_t elapsed = server.unixtime - c->obuf_soft_limit_reached_time;

            if (elapsed <=
                server.client_obuf_limits[class].soft_limit_seconds) {
                soft = 0; /* The client still did not reached the max number of
                             seconds for the soft limit to be considered
                             reached. */
            }
        }
    } else {
        c->obuf_soft_limit_reached_time = 0;
    }
    return soft || hard;
}

/* Asynchronously close a client if soft or hard limit is reached on the
 * output buffer size. The caller can check if the client will be closed
 * checking if the client CLIENT_CLOSE_ASAP flag is set.
 *
 * Note: we need to close the client asynchronously because this function is
 * called from contexts where the client can't be freed safely, i.e. from the
 * lower level functions pushing data inside the client output buffers. */
void asyncCloseClientOnOutputBufferLimitReached(client *c) {
    if (c->fd == -1) return; /* It is unsafe to free fake clients. */
    serverAssert(c->reply_bytes < SIZE_MAX - (1024 * 64));
    if (c->reply_bytes == 0 || c->flags & CLIENT_CLOSE_ASAP) return;
    if (checkClientOutputBufferLimits(c)) {
        sds client = catClientInfoString(sdsempty(), c);

        freeClientAsync(c);
        serverLog(LL_WARNING, "Client %s scheduled to be closed ASAP for overcoming of output buffer limits.", client);
        sdsfree(client);
    }
}

/* Helper function used by freeMemoryIfNeeded() in order to flush slaves
 * output buffers without returning control to the event loop.
 * This is also called by SHUTDOWN for a best-effort attempt to send
 * slaves the latest writes. */
void flushSlavesOutputBuffers(void) {
    listIter li;
    listNode *ln;

    listRewind(server.slaves, &li);
    while ((ln = listNext(&li))) {
        client *slave = listNodeValue(ln);
        int events = aeGetFileEvents(server.el, slave->fd);
        int can_receive_writes = (events & AE_WRITABLE) ||
                                 (slave->flags & CLIENT_PENDING_WRITE);

        /* We don't want to send the pending data to the replica in a few
         * cases:
         *
         * 1. For some reason there is neither the write handler installed
         *    nor the client is flagged as to have pending writes: for some
         *    reason this replica may not be set to receive data. This is
         *    just for the sake of defensive programming.
         *
         * 2. The put_online_on_ack flag is true. To know why we don't want
         *    to send data to the replica in this case, please grep for the
         *    flag for this flag.
         *
         * 3. Obviously if the slave is not ONLINE.
         */
        if (slave->replstate == SLAVE_STATE_ONLINE &&
            can_receive_writes &&
            !slave->repl_put_online_on_ack &&
            clientHasPendingReplies(slave)) {
            writeToClient(slave->fd, slave, 0);
        }
    }
}

/* Pause clients up to the specified unixtime (in ms). While clients
 * are paused no command is processed from clients, so the data set can't
 * change during that time.
 *
 * However while this function pauses normal and Pub/Sub clients, slaves are
 * still served, so this function can be used on server upgrades where it is
 * required that slaves process the latest bytes from the replication stream
 * before being turned to masters.
 *
 * This function is also internally used by Redis Cluster for the manual
 * failover procedure implemented by CLUSTER FAILOVER.
 *
 * The function always succeed, even if there is already a pause in progress.
 * In such a case, the pause is extended if the duration is more than the
 * time left for the previous duration. However if the duration is smaller
 * than the time left for the previous pause, no change is made to the
 * left duration. */
void pauseClients(mstime_t end) {
    if (!server.clients_paused || end > server.clients_pause_end_time)
        server.clients_pause_end_time = end;
    server.clients_paused = 1;
}

int clientsArePaused(void) {
    /* 判断服务器是否处于pause状态, 并检查暂停的时间是否已过期 */
    if (server.clients_paused &&
        server.clients_pause_end_time < server.mstime) {
        listNode *ln;
        listIter li;
        client *c;

        server.clients_paused = 0;

        /* 将所有的客户端放入未阻塞客户端队列中，以强制重新处理输入缓冲区（如果有的话） */
        listRewind(server.clients, &li);
        while ((ln = listNext(&li)) != NULL) {
            c = listNodeValue(ln);

            /* 不要处理从属节点和阻塞的客户端，
            后者的挂起请求将在解除阻塞时处理 */
            if (c->flags & (CLIENT_SLAVE | CLIENT_BLOCKED)) continue;
            queueClientForReprocessing(c); // 将客户端添加到重新处理队列中
        }
    }
    return server.clients_paused; // 返回服务器当前的暂停状态
}

/* This function is called by Redis in order to process a few events from
 * time to time while blocked into some not interruptible operation.
 * This allows to reply to clients with the -LOADING error while loading the
 * data set at startup or after a full resynchronization with the master
 * and so forth.
 *
 * It calls the event loop in order to process a few events. Specifically we
 * try to call the event loop 4 times as long as we receive acknowledge that
 * some event was processed, in order to go forward with the accept, read,
 * write, close sequence needed to serve a client.
 *
 * The function returns the total number of events processed. */
int processEventsWhileBlocked(void) {
    int iterations = 4; /* See the function top-comment. */
    int count = 0;
    while (iterations--) {
        int events = 0;
        events += aeProcessEvents(server.el, AE_FILE_EVENTS | AE_DONT_WAIT);
        events += handleClientsWithPendingWrites();
        if (!events) break;
        count += events;
    }
    return count;
}
