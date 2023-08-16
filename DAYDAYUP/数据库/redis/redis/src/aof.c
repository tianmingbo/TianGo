#include "server.h"
#include "bio.h"
#include "rio.h"

#include <signal.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <sys/param.h>

void aofUpdateCurrentSize(void);

void aofClosePipes(void);

/* ----------------------------------------------------------------------------
 * AOF rewrite buffer implementation.
 *
 * The following code implement a simple buffer used in order to accumulate
 * changes while the background process is rewriting the AOF file.
 *
 * We only need to append, but can't just use realloc with a large block
 * because 'huge' reallocs are not always handled as one could expect
 * (via remapping of pages at OS level) but may involve copying data.
 *
 * For this reason we use a list of blocks, every block is
 * AOF_RW_BUF_BLOCK_SIZE bytes.
 * ------------------------------------------------------------------------- */

#define AOF_RW_BUF_BLOCK_SIZE (1024*1024*10)    /* 10 MB per block */

typedef struct aofrwblock {
    unsigned long used, free; //buf数组已用空间和剩余空间
    char buf[AOF_RW_BUF_BLOCK_SIZE]; //默认10MB
} aofrwblock;

/* 如果需要，此函数会释放旧的 AOF 重写缓冲区，并初始化一个新的缓冲区。
 * 它测试 server.aof_rewrite_buf_blocks 是否等于 NULL，
 * 因此也可以用于第一次初始化。 */
void aofRewriteBufferReset(void) {
    if (server.aof_rewrite_buf_blocks)
        listRelease(server.aof_rewrite_buf_blocks);

    server.aof_rewrite_buf_blocks = listCreate();
    listSetFreeMethod(server.aof_rewrite_buf_blocks, zfree);
}

/* Return the current size of the AOF rewrite buffer. */
unsigned long aofRewriteBufferSize(void) {
    listNode *ln;
    listIter li;
    unsigned long size = 0;

    listRewind(server.aof_rewrite_buf_blocks, &li);
    while ((ln = listNext(&li))) {
        aofrwblock *block = listNodeValue(ln);
        size += block->used;
    }
    return size;
}

/* 从aof_rewrite_buf_blocks中逐个取出block,
 * 通过aof_pipe_write_data_to_child管道,将block中的命令发给重写子进程
 * */
void aofChildWriteDiffData(aeEventLoop *el, int fd, void *privdata, int mask) {
    listNode *ln;
    aofrwblock *block;
    ssize_t nwritten;
    UNUSED(el);
    UNUSED(fd);
    UNUSED(privdata);
    UNUSED(mask);

    while (1) {
        ln = listFirst(server.aof_rewrite_buf_blocks);
        block = ln ? ln->value : NULL;
        if (server.aof_stop_sending_diff || !block) {
            aeDeleteFileEvent(server.el, server.aof_pipe_write_data_to_child,
                              AE_WRITABLE);
            return;
        }
        if (block->used > 0) {
            //将数据块写入主进程和重写子进程间的管道
            nwritten = write(server.aof_pipe_write_data_to_child,
                             block->buf, block->used);
            if (nwritten <= 0) return;
            memmove(block->buf, block->buf + nwritten, block->used - nwritten);
            block->used -= nwritten;
            block->free += nwritten;
        }
        if (block->used == 0) listDelNode(server.aof_rewrite_buf_blocks, ln);
    }
}

/* Append data to the AOF rewrite buffer, allocating new blocks if needed. */
void aofRewriteBufferAppend(unsigned char *s, unsigned long len) {
    listNode *ln = listLast(server.aof_rewrite_buf_blocks);
    aofrwblock *block = ln ? ln->value : NULL;

    while (len) {
        /* If we already got at least an allocated block, try appending
         * at least some piece into it. */
        if (block) {
            unsigned long thislen = (block->free < len) ? block->free : len;
            if (thislen) {  /* The current block is not already full. */
                memcpy(block->buf + block->used, s, thislen);
                block->used += thislen;
                block->free -= thislen;
                s += thislen;
                len -= thislen;
            }
        }

        if (len) { /* 新申请一个block,或第一个block */
            int numblocks;

            block = zmalloc(sizeof(*block));
            block->free = AOF_RW_BUF_BLOCK_SIZE;
            block->used = 0;
            //将这些数据块拼接起来
            listAddNodeTail(server.aof_rewrite_buf_blocks, block);

            /* 每次跨越超过 10 个或 100 个区块时，分别记录为通知或警告。 */
            numblocks = listLength(server.aof_rewrite_buf_blocks);
            if (((numblocks + 1) % 10) == 0) {
                int level = ((numblocks + 1) % 100) == 0 ? LL_WARNING :
                            LL_NOTICE;
                serverLog(level, "Background AOF buffer size: %lu MB",
                          aofRewriteBufferSize() / (1024 * 1024));
            }
        }
    }

    /* 检查aof_pipe_write_data_to_child是否注册了写事件 */
    if (aeGetFileEvents(server.el, server.aof_pipe_write_data_to_child) == 0) {
        //新注册一个写事件
        aeCreateFileEvent(server.el, server.aof_pipe_write_data_to_child,
                          AE_WRITABLE, aofChildWriteDiffData, NULL);
    }
}

/* Write the buffer (possibly composed of multiple blocks) into the specified
 * fd. If a short write or any other error happens -1 is returned,
 * otherwise the number of bytes written is returned. */
ssize_t aofRewriteBufferWrite(int fd) {
    listNode *ln;
    listIter li;
    ssize_t count = 0;

    listRewind(server.aof_rewrite_buf_blocks, &li);
    while ((ln = listNext(&li))) {
        aofrwblock *block = listNodeValue(ln);
        ssize_t nwritten;

        if (block->used) {
            nwritten = write(fd, block->buf, block->used);
            if (nwritten != (ssize_t) block->used) {
                if (nwritten == 0) errno = EIO;
                return -1;
            }
            count += nwritten;
        }
    }
    return count;
}

/* ----------------------------------------------------------------------------
 * AOF file implementation
 * ------------------------------------------------------------------------- */

/* Return true if an AOf fsync is currently already in progress in a
 * BIO thread. */
int aofFsyncInProgress(void) {
    return bioPendingJobsOfType(BIO_AOF_FSYNC) != 0;
}

/* Starts a background task that performs fsync() against the specified
 * file descriptor (the one of the AOF file) in another thread. */
void aof_background_fsync(int fd) {
    bioCreateBackgroundJob(BIO_AOF_FSYNC, (void *) (long) fd, NULL, NULL);
}

/* Kills an AOFRW child process if exists */
static void killAppendOnlyChild(void) {
    int statloc;
    /* No AOFRW child? return. */
    if (server.aof_child_pid == -1) return;
    /* Kill AOFRW child, wait for child exit. */
    serverLog(LL_NOTICE, "Killing running AOF rewrite child: %ld",
              (long) server.aof_child_pid);
    if (kill(server.aof_child_pid, SIGUSR1) != -1) {
        while (wait3(&statloc, 0, NULL) != server.aof_child_pid);
    }
    /* Reset the buffer accumulating changes while the child saves. */
    aofRewriteBufferReset();
    aofRemoveTempFile(server.aof_child_pid);
    server.aof_child_pid = -1;
    server.aof_rewrite_time_start = -1;
    /* Close pipes used for IPC between the two processes. */
    aofClosePipes();
}

/* Called when the user switches from "appendonly yes" to "appendonly no"
 * at runtime using the CONFIG command. */
void stopAppendOnly(void) {
    serverAssert(server.aof_state != AOF_OFF);
    flushAppendOnlyFile(1);
    redis_fsync(server.aof_fd);
    close(server.aof_fd);

    server.aof_fd = -1;
    server.aof_selected_db = -1;
    server.aof_state = AOF_OFF;
    killAppendOnlyChild();
}

/* config set appendonly yes 时调用 */
int startAppendOnly(void) {
    char cwd[MAXPATHLEN]; /* Current working dir path for error messages. */
    int newfd;

    newfd = open(server.aof_filename, O_WRONLY | O_APPEND | O_CREAT, 0644);
    serverAssert(server.aof_state == AOF_OFF);
    if (newfd == -1) {
        char *cwdp = getcwd(cwd, MAXPATHLEN);

        serverLog(LL_WARNING,
                  "Redis needs to enable the AOF but can't open the "
                  "append only file %s (in server root dir %s): %s",
                  server.aof_filename,
                  cwdp ? cwdp : "unknown",
                  strerror(errno));
        return C_ERR;
    }
    if (server.rdb_child_pid != -1) {
        //是否有rdb子进程
        server.aof_rewrite_scheduled = 1; //将aof重写设置为待调度执行
        serverLog(LL_WARNING,
                  "AOF was enabled but there is already a child process saving an RDB file on disk. An AOF background was scheduled to start when possible.");
    } else {
        /* If there is a pending AOF rewrite, we need to switch it off and
         * start a new one: the old one cannot be reused because it is not
         * accumulating the AOF buffer. */
        if (server.aof_child_pid != -1) {
            //检测到有aof重写子进程在执行,先kill子进程
            serverLog(LL_WARNING,
                      "AOF was enabled but there is already an AOF rewriting in background. Stopping background AOF and starting a rewrite now.");
            killAppendOnlyChild();
        }
        if (rewriteAppendOnlyFileBackground() == C_ERR) {
            close(newfd);
            serverLog(LL_WARNING,
                      "Redis needs to enable the AOF but can't trigger a background AOF rewrite operation. Check the above logs for more info about the error.");
            return C_ERR;
        }
    }
    /* We correctly switched on AOF, now wait for the rewrite to be complete
     * in order to append data on disk. */
    server.aof_state = AOF_WAIT_REWRITE;
    server.aof_last_fsync = server.unixtime;
    server.aof_fd = newfd;
    return C_OK;
}

/* This is a wrapper to the write syscall in order to retry on short writes
 * or if the syscall gets interrupted. It could look strange that we retry
 * on short writes given that we are writing to a block device: normally if
 * the first call is short, there is a end-of-space condition, so the next
 * is likely to fail. However apparently in modern systems this is no longer
 * true, and in general it looks just more resilient to retry the write. If
 * there is an actual error condition we'll get it at the next try. */
ssize_t aofWrite(int fd, const char *buf, size_t len) {
    ssize_t nwritten = 0, totwritten = 0;

    while (len) {
        nwritten = write(fd, buf, len);

        if (nwritten < 0) {
            if (errno == EINTR) {
                continue;
            }
            return totwritten ? totwritten : -1;
        }

        len -= nwritten;
        buf += nwritten;
        totwritten += nwritten;
    }

    return totwritten;
}

/* Write the append only file buffer on disk.
 */
#define AOF_WRITE_LOG_ERROR_RATE 30 /* Seconds between errors logging. */

void flushAppendOnlyFile(int force) {
    ssize_t nwritten;
    int sync_in_progress = 0;
    mstime_t latency;

    //当aof缓冲区为空
    if (sdslen(server.aof_buf) == 0) {
        /* 如果磁盘同步策略为每秒同步,并且当前存在待同步磁盘的数据,距离上次磁盘同步过去了1s
         * 则执行磁盘同步
         * */
        if (server.aof_fsync == AOF_FSYNC_EVERYSEC &&
            server.aof_fsync_offset != server.aof_current_size &&
            server.unixtime > server.aof_last_fsync &&
            !(sync_in_progress = aofFsyncInProgress())) {
            goto try_fsync;
        } else {
            return;
        }
    }

    //函数检查当前是否存在后台线程正在同步磁盘
    if (server.aof_fsync == AOF_FSYNC_EVERYSEC)
        sync_in_progress = aofFsyncInProgress();

    if (server.aof_fsync == AOF_FSYNC_EVERYSEC && !force) {
        /* 如果磁盘同步为每秒同步,则延迟该AOF缓冲区刷新 */
        if (sync_in_progress) {
            if (server.aof_flush_postponed_start == 0) {
                server.aof_flush_postponed_start = server.unixtime;
                return;
            } else if (server.unixtime - server.aof_flush_postponed_start < 2) {
                /* 如果已经延迟多次,且延迟时间超过2s,则强制刷新aof缓冲区 */
                return;
            }
            /* Otherwise fall trough, and go write since we can't wait
             * over two seconds. */
            server.aof_delayed_fsync++;
            serverLog(LL_NOTICE,
                      "Asynchronous AOF fsync is taking too long (disk is busy?). Writing the AOF buffer without waiting for fsync to complete, this may slow down Redis.");
        }
    }

    latencyStartMonitor(latency);
    //将aof缓冲区内容写入文件
    nwritten = aofWrite(server.aof_fd, server.aof_buf, sdslen(server.aof_buf));
    latencyEndMonitor(latency);
    /* We want to capture different events for delayed writes:
     * when the delay happens with a pending fsync, or with a saving child
     * active, and when the above two conditions are missing.
     * We also use an additional event name to save all samples which is
     * useful for graphing / monitoring purposes. */
    if (sync_in_progress) {
        latencyAddSampleIfNeeded("aof-write-pending-fsync", latency);
    } else if (server.aof_child_pid != -1 || server.rdb_child_pid != -1) {
        latencyAddSampleIfNeeded("aof-write-active-child", latency);
    } else {
        latencyAddSampleIfNeeded("aof-write-alone", latency);
    }
    latencyAddSampleIfNeeded("aof-write", latency);

    /* We performed the write so reset the postponed flush sentinel to zero. */
    server.aof_flush_postponed_start = 0;

    if (nwritten != (ssize_t) sdslen(server.aof_buf)) {
        static time_t last_write_error_log = 0;
        int can_log = 0;

        /* Limit logging rate to 1 line per AOF_WRITE_LOG_ERROR_RATE seconds. */
        if ((server.unixtime - last_write_error_log) > AOF_WRITE_LOG_ERROR_RATE) {
            can_log = 1;
            last_write_error_log = server.unixtime;
        }

        /* Log the AOF write error and record the error code. */
        if (nwritten == -1) {
            if (can_log) {
                serverLog(LL_WARNING, "Error writing to the AOF file: %s",
                          strerror(errno));
                server.aof_last_write_errno = errno;
            }
        } else {
            if (can_log) {
                serverLog(LL_WARNING, "Short write while writing to "
                                      "the AOF file: (nwritten=%lld, "
                                      "expected=%lld)",
                          (long long) nwritten,
                          (long long) sdslen(server.aof_buf));
            }

            if (ftruncate(server.aof_fd, server.aof_current_size) == -1) {
                if (can_log) {
                    serverLog(LL_WARNING, "Could not remove short write "
                                          "from the append-only file.  Redis may refuse "
                                          "to load the AOF the next time it starts.  "
                                          "ftruncate: %s", strerror(errno));
                }
            } else {
                /* If the ftruncate() succeeded we can set nwritten to
                 * -1 since there is no longer partial data into the AOF. */
                nwritten = -1;
            }
            server.aof_last_write_errno = ENOSPC;
        }

        /* Handle the AOF write error. */
        if (server.aof_fsync == AOF_FSYNC_ALWAYS) {
            /* We can't recover when the fsync policy is ALWAYS since the
             * reply for the client is already in the output buffers, and we
             * have the contract with the user that on acknowledged write data
             * is synced on disk. */
            serverLog(LL_WARNING,
                      "Can't recover from AOF write error when the AOF fsync policy is 'always'. Exiting...");
            exit(1);
        } else {
            /* Recover from failed write leaving data into the buffer. However
             * set an error to stop accepting writes as long as the error
             * condition is not cleared. */
            server.aof_last_write_status = C_ERR;

            /* Trim the sds buffer if there was a partial write, and there
             * was no way to undo it with ftruncate(2). */
            if (nwritten > 0) {
                server.aof_current_size += nwritten;
                sdsrange(server.aof_buf, nwritten, -1);
            }
            return; /* We'll try again on the next call... */
        }
    } else {
        /* Successful write(2). If AOF was in error state, restore the
         * OK state and log the event. */
        if (server.aof_last_write_status == C_ERR) {
            serverLog(LL_WARNING,
                      "AOF write error looks solved, Redis can write again.");
            server.aof_last_write_status = C_OK;
        }
    }
    server.aof_current_size += nwritten;

    /* 如果aof总空间小于4KB,清空内容并重用 */
    if ((sdslen(server.aof_buf) + sdsavail(server.aof_buf)) < 4000) {
        sdsclear(server.aof_buf);
    } else {
        sdsfree(server.aof_buf);
        server.aof_buf = sdsempty();
    }

    try_fsync:
    /* 如果存在rdb或重写子进程,且开启了aof_no_fsync_on_rewrite,则不同步磁盘 */
    if (server.aof_no_fsync_on_rewrite &&
        (server.aof_child_pid != -1 || server.rdb_child_pid != -1))
        return;

    /* 每次都同步*/
    if (server.aof_fsync == AOF_FSYNC_ALWAYS) {
        /* redis_fsync is defined as fdatasync() for Linux in order to avoid
         * flushing metadata. */
        latencyStartMonitor(latency);
        //redis_fsync在linux下调用fdatasync,其它系统调用fsync
        redis_fsync(server.aof_fd); /* Let's try to get this data on the disk */
        latencyEndMonitor(latency);
        latencyAddSampleIfNeeded("aof-fsync-always", latency);
        server.aof_fsync_offset = server.aof_current_size;
        server.aof_last_fsync = server.unixtime;
    } else if ((server.aof_fsync == AOF_FSYNC_EVERYSEC &&
                server.unixtime > server.aof_last_fsync)) {
        if (!sync_in_progress) {
            //每秒同步,则添加一个后台任务负责同步磁盘
            aof_background_fsync(server.aof_fd);
            server.aof_fsync_offset = server.aof_current_size;
        }
        server.aof_last_fsync = server.unixtime;
    }
}

sds catAppendOnlyGenericCommand(sds dst, int argc, robj **argv) {
    char buf[32];
    int len, j;
    robj *o;

    buf[0] = '*';
    len = 1 + ll2string(buf + 1, sizeof(buf) - 1, argc);
    buf[len++] = '\r';
    buf[len++] = '\n';
    dst = sdscatlen(dst, buf, len);

    for (j = 0; j < argc; j++) {
        o = getDecodedObject(argv[j]);
        buf[0] = '$';
        len = 1 + ll2string(buf + 1, sizeof(buf) - 1, sdslen(o->ptr));
        buf[len++] = '\r';
        buf[len++] = '\n';
        dst = sdscatlen(dst, buf, len);
        dst = sdscatlen(dst, o->ptr, sdslen(o->ptr));
        dst = sdscatlen(dst, "\r\n", 2);
        decrRefCount(o);
    }
    return dst;
}

/* 将 EXPIRE 和 PEXPIRE 命令转换为 PEXPIREAT 命令，
 * 以便在aof文件中保留精度，并且时间始终是绝对的而不是相对的 */
sds catAppendOnlyExpireAtCommand(sds buf, struct redisCommand *cmd, robj *key, robj *seconds) {
    long long when;
    robj *argv[3];

    /* Make sure we can use strtoll */
    seconds = getDecodedObject(seconds);
    when = strtoll(seconds->ptr, NULL, 10);
    /* Convert argument into milliseconds for EXPIRE, SETEX, EXPIREAT */
    if (cmd->proc == expireCommand || cmd->proc == setexCommand ||
        cmd->proc == expireatCommand) {
        when *= 1000;
    }
    /* Convert into absolute time for EXPIRE, PEXPIRE, SETEX, PSETEX */
    if (cmd->proc == expireCommand || cmd->proc == pexpireCommand ||
        cmd->proc == setexCommand || cmd->proc == psetexCommand) {
        when += mstime();
    }
    decrRefCount(seconds);

    argv[0] = createStringObject("PEXPIREAT", 9);
    argv[1] = key;
    argv[2] = createStringObjectFromLongLong(when);
    buf = catAppendOnlyGenericCommand(buf, 3, argv);
    decrRefCount(argv[0]);
    decrRefCount(argv[2]);
    return buf;
}

//追加写请求到aof文件
void feedAppendOnlyFile(struct redisCommand *cmd, int dictid, robj **argv, int argc) {
    sds buf = sdsempty();
    robj *tmpargv[3];

    /* The DB this command was targeting is not the same as the last command
     * we appended. To issue a SELECT command is needed. */
    if (dictid != server.aof_selected_db) {
        char seldb[64];

        snprintf(seldb, sizeof(seldb), "%d", dictid);
        buf = sdscatprintf(buf, "*2\r\n$6\r\nSELECT\r\n$%lu\r\n%s\r\n",
                           (unsigned long) strlen(seldb), seldb);
        server.aof_selected_db = dictid;
    }
    // 对键带过期时间特殊处理,转成PEXPIREAT
    if (cmd->proc == expireCommand || cmd->proc == pexpireCommand ||
        cmd->proc == expireatCommand) {
        /* Translate EXPIRE/PEXPIRE/EXPIREAT into PEXPIREAT */
        buf = catAppendOnlyExpireAtCommand(buf, cmd, argv[1], argv[2]);
    } else if (cmd->proc == setexCommand || cmd->proc == psetexCommand) {
        /* Translate SETEX/PSETEX to SET and PEXPIREAT */
        tmpargv[0] = createStringObject("SET", 3);
        tmpargv[1] = argv[1];
        tmpargv[2] = argv[3];
        buf = catAppendOnlyGenericCommand(buf, 3, tmpargv);
        decrRefCount(tmpargv[0]);
        buf = catAppendOnlyExpireAtCommand(buf, cmd, argv[1], argv[2]);
    } else if (cmd->proc == setCommand && argc > 3) {
        int i;
        robj *exarg = NULL, *pxarg = NULL;
        /* Translate SET [EX seconds][PX milliseconds] to SET and PEXPIREAT */
        buf = catAppendOnlyGenericCommand(buf, 3, argv);
        for (i = 3; i < argc; i++) {
            if (!strcasecmp(argv[i]->ptr, "ex")) exarg = argv[i + 1];
            if (!strcasecmp(argv[i]->ptr, "px")) pxarg = argv[i + 1];
        }
        serverAssert(!(exarg && pxarg));
        if (exarg)
            buf = catAppendOnlyExpireAtCommand(buf, server.expireCommand, argv[1],
                                               exarg);
        if (pxarg)
            buf = catAppendOnlyExpireAtCommand(buf, server.pexpireCommand, argv[1],
                                               pxarg);
    } else {
        /* All the other commands don't need translation or need the
         * same translation already operated in the command vector
         * for the replication itself. */
        buf = catAppendOnlyGenericCommand(buf, argc, argv);
    }

    /* 如果开启了aof,则将buf暂存区内容写入aof buf */
    if (server.aof_state == AOF_ON)
        server.aof_buf = sdscatlen(server.aof_buf, buf, sdslen(buf));

    //如果当前存在子进程在重写aof,还需要将bug暂存区内容写入重写缓冲区aof_rewrite_buf_blocks
    if (server.aof_child_pid != -1)
        aofRewriteBufferAppend((unsigned char *) buf, sdslen(buf));

    sdsfree(buf);
}

/* ----------------------------------------------------------------------------
 * AOF loading
 * ------------------------------------------------------------------------- */

/* In Redis commands are always executed in the context of a client, so in
 * order to load the append only file we need to create a fake client. */
struct client *createFakeClient(void) {
    struct client *c = zmalloc(sizeof(*c));

    selectDb(c, 0);
    c->fd = -1;
    c->name = NULL;
    c->querybuf = sdsempty();
    c->querybuf_peak = 0;
    c->argc = 0;
    c->argv = NULL;
    c->bufpos = 0;
    c->flags = 0;
    c->btype = BLOCKED_NONE;
    /* We set the fake client as a slave waiting for the synchronization
     * so that Redis will not try to send replies to this client. */
    c->replstate = SLAVE_STATE_WAIT_BGSAVE_START;
    c->reply = listCreate();
    c->reply_bytes = 0;
    c->obuf_soft_limit_reached_time = 0;
    c->watched_keys = listCreate();
    c->peerid = NULL;
    listSetFreeMethod(c->reply, freeClientReplyValue);
    listSetDupMethod(c->reply, dupClientReplyValue);
    initClientMultiState(c);
    return c;
}

void freeFakeClientArgv(struct client *c) {
    int j;

    for (j = 0; j < c->argc; j++)
        decrRefCount(c->argv[j]);
    zfree(c->argv);
}

void freeFakeClient(struct client *c) {
    sdsfree(c->querybuf);
    listRelease(c->reply);
    listRelease(c->watched_keys);
    freeClientMultiState(c);
    zfree(c);
}

/* Replay the append log file. On success C_OK is returned. On non fatal
 * error (the append only file is zero-length) C_ERR is returned. On
 * fatal error an error message is logged and the program exists. */
int loadAppendOnlyFile(char *filename) {
    struct client *fakeClient;
    FILE *fp = fopen(filename, "r");
    struct redis_stat sb;
    int old_aof_state = server.aof_state;
    long loops = 0;
    off_t valid_up_to = 0; /* Offset of latest well-formed command loaded. */
    off_t valid_before_multi = 0; /* Offset before MULTI command loaded. */

    if (fp == NULL) {
        serverLog(LL_WARNING, "Fatal error: can't open the append log file for reading: %s", strerror(errno));
        exit(1);
    }

    /* Handle a zero-length AOF file as a special case. An empty AOF file
     * is a valid AOF because an empty server with AOF enabled will create
     * a zero length file at startup, that will remain like that if no write
     * operation is received. */
    if (fp && redis_fstat(fileno(fp), &sb) != -1 && sb.st_size == 0) {
        server.aof_current_size = 0;
        server.aof_fsync_offset = server.aof_current_size;
        fclose(fp);
        return C_ERR;
    }

    /* Temporarily disable AOF, to prevent EXEC from feeding a MULTI
     * to the same file we're about to read. */
    server.aof_state = AOF_OFF;

    fakeClient = createFakeClient();
    startLoading(fp);

    /* Check if this AOF file has an RDB preamble. In that case we need to
     * load the RDB file and later continue loading the AOF tail. */
    char sig[5]; /* "REDIS" */
    if (fread(sig, 1, 5, fp) != 5 || memcmp(sig, "REDIS", 5) != 0) {
        /* No RDB preamble, seek back at 0 offset. */
        if (fseek(fp, 0, SEEK_SET) == -1) goto readerr;
    } else {
        /* RDB preamble. Pass loading the RDB functions. */
        rio rdb;

        serverLog(LL_NOTICE, "Reading RDB preamble from AOF file...");
        if (fseek(fp, 0, SEEK_SET) == -1) goto readerr;
        rioInitWithFile(&rdb, fp);
        if (rdbLoadRio(&rdb, NULL, 1) != C_OK) {
            serverLog(LL_WARNING, "Error reading the RDB preamble of the AOF file, AOF loading aborted");
            goto readerr;
        } else {
            serverLog(LL_NOTICE, "Reading the remaining AOF tail...");
        }
    }

    /* Read the actual AOF file, in REPL format, command by command. */
    while (1) {
        int argc, j;
        unsigned long len;
        robj **argv;
        char buf[128];
        sds argsds;
        struct redisCommand *cmd;

        /* Serve the clients from time to time */
        if (!(loops++ % 1000)) {
            loadingProgress(ftello(fp));
            processEventsWhileBlocked();
        }

        if (fgets(buf, sizeof(buf), fp) == NULL) {
            if (feof(fp))
                break;
            else
                goto readerr;
        }
        if (buf[0] != '*') goto fmterr;
        if (buf[1] == '\0') goto readerr;
        argc = atoi(buf + 1);
        if (argc < 1) goto fmterr;

        /* Load the next command in the AOF as our fake client
         * argv. */
        argv = zmalloc(sizeof(robj *) * argc);
        fakeClient->argc = argc;
        fakeClient->argv = argv;

        for (j = 0; j < argc; j++) {
            /* Parse the argument len. */
            char *readres = fgets(buf, sizeof(buf), fp);
            if (readres == NULL || buf[0] != '$') {
                fakeClient->argc = j; /* Free up to j-1. */
                freeFakeClientArgv(fakeClient);
                if (readres == NULL)
                    goto readerr;
                else
                    goto fmterr;
            }
            len = strtol(buf + 1, NULL, 10);

            /* Read it into a string object. */
            argsds = sdsnewlen(SDS_NOINIT, len);
            if (len && fread(argsds, len, 1, fp) == 0) {
                sdsfree(argsds);
                fakeClient->argc = j; /* Free up to j-1. */
                freeFakeClientArgv(fakeClient);
                goto readerr;
            }
            argv[j] = createObject(OBJ_STRING, argsds);

            /* Discard CRLF. */
            if (fread(buf, 2, 1, fp) == 0) {
                fakeClient->argc = j + 1; /* Free up to j. */
                freeFakeClientArgv(fakeClient);
                goto readerr;
            }
        }

        /* Command lookup */
        cmd = lookupCommand(argv[0]->ptr);
        if (!cmd) {
            serverLog(LL_WARNING,
                      "Unknown command '%s' reading the append only file",
                      (char *) argv[0]->ptr);
            exit(1);
        }

        if (cmd == server.multiCommand) valid_before_multi = valid_up_to;

        /* Run the command in the context of a fake client */
        fakeClient->cmd = cmd;
        if (fakeClient->flags & CLIENT_MULTI &&
            fakeClient->cmd->proc != execCommand) {
            queueMultiCommand(fakeClient);
        } else {
            cmd->proc(fakeClient);
        }

        /* The fake client should not have a reply */
        serverAssert(fakeClient->bufpos == 0 &&
                     listLength(fakeClient->reply) == 0);

        /* The fake client should never get blocked */
        serverAssert((fakeClient->flags & CLIENT_BLOCKED) == 0);

        /* Clean up. Command code may have changed argv/argc so we use the
         * argv/argc of the client instead of the local variables. */
        freeFakeClientArgv(fakeClient);
        fakeClient->cmd = NULL;
        if (server.aof_load_truncated) valid_up_to = ftello(fp);
    }

    /* This point can only be reached when EOF is reached without errors.
     * If the client is in the middle of a MULTI/EXEC, handle it as it was
     * a short read, even if technically the protocol is correct: we want
     * to remove the unprocessed tail and continue. */
    if (fakeClient->flags & CLIENT_MULTI) {
        serverLog(LL_WARNING,
                  "Revert incomplete MULTI/EXEC transaction in AOF file");
        valid_up_to = valid_before_multi;
        goto uxeof;
    }

    loaded_ok: /* DB loaded, cleanup and return C_OK to the caller. */
    fclose(fp);
    freeFakeClient(fakeClient);
    server.aof_state = old_aof_state;
    stopLoading();
    aofUpdateCurrentSize();
    server.aof_rewrite_base_size = server.aof_current_size;
    server.aof_fsync_offset = server.aof_current_size;
    return C_OK;

    readerr: /* Read error. If feof(fp) is true, fall through to unexpected EOF. */
    if (!feof(fp)) {
        if (fakeClient) freeFakeClient(fakeClient); /* avoid valgrind warning */
        serverLog(LL_WARNING, "Unrecoverable error reading the append only file: %s", strerror(errno));
        exit(1);
    }

    uxeof: /* Unexpected AOF end of file. */
    if (server.aof_load_truncated) {
        serverLog(LL_WARNING, "!!! Warning: short read while loading the AOF file !!!");
        serverLog(LL_WARNING, "!!! Truncating the AOF at offset %llu !!!",
                  (unsigned long long) valid_up_to);
        if (valid_up_to == -1 || truncate(filename, valid_up_to) == -1) {
            if (valid_up_to == -1) {
                serverLog(LL_WARNING, "Last valid command offset is invalid");
            } else {
                serverLog(LL_WARNING, "Error truncating the AOF file: %s",
                          strerror(errno));
            }
        } else {
            /* Make sure the AOF file descriptor points to the end of the
             * file after the truncate call. */
            if (server.aof_fd != -1 && lseek(server.aof_fd, 0, SEEK_END) == -1) {
                serverLog(LL_WARNING, "Can't seek the end of the AOF file: %s",
                          strerror(errno));
            } else {
                serverLog(LL_WARNING,
                          "AOF loaded anyway because aof-load-truncated is enabled");
                goto loaded_ok;
            }
        }
    }
    if (fakeClient) freeFakeClient(fakeClient); /* avoid valgrind warning */
    serverLog(LL_WARNING,
              "Unexpected end of file reading the append only file. You can: 1) Make a backup of your AOF file, then use ./redis-check-aof --fix <filename>. 2) Alternatively you can set the 'aof-load-truncated' configuration option to yes and restart the server.");
    exit(1);

    fmterr: /* Format error. */
    if (fakeClient) freeFakeClient(fakeClient); /* avoid valgrind warning */
    serverLog(LL_WARNING,
              "Bad file format reading the append only file: make a backup of your AOF file, then use ./redis-check-aof --fix <filename>");
    exit(1);
}

/* ----------------------------------------------------------------------------
 * AOF rewrite
 * ------------------------------------------------------------------------- */

/* Delegate writing an object to writing a bulk string or bulk long long.
 * This is not placed in rio.c since that adds the server.h dependency. */
int rioWriteBulkObject(rio *r, robj *obj) {
    /* Avoid using getDecodedObject to help copy-on-write (we are often
     * in a child process when this function is called). */
    if (obj->encoding == OBJ_ENCODING_INT) {
        return rioWriteBulkLongLong(r, (long) obj->ptr);
    } else if (sdsEncodedObject(obj)) {
        return rioWriteBulkString(r, obj->ptr, sdslen(obj->ptr));
    } else {
        serverPanic("Unknown string encoding");
    }
}

/* Emit the commands needed to rebuild a list object.
 * The function returns 0 on error, 1 on success. */
int rewriteListObject(rio *r, robj *key, robj *o) {
    long long count = 0, items = listTypeLength(o);

    if (o->encoding == OBJ_ENCODING_QUICKLIST) {
        quicklist *list = o->ptr;
        quicklistIter *li = quicklistGetIterator(list, AL_START_HEAD);
        quicklistEntry entry;

        while (quicklistNext(li, &entry)) {
            if (count == 0) {
                int cmd_items = (items > AOF_REWRITE_ITEMS_PER_CMD) ?
                                AOF_REWRITE_ITEMS_PER_CMD : items;
                if (rioWriteBulkCount(r, '*', 2 + cmd_items) == 0) return 0;
                if (rioWriteBulkString(r, "RPUSH", 5) == 0) return 0;
                if (rioWriteBulkObject(r, key) == 0) return 0;
            }

            if (entry.value) {
                if (rioWriteBulkString(r, (char *) entry.value, entry.sz) == 0) return 0;
            } else {
                if (rioWriteBulkLongLong(r, entry.longval) == 0) return 0;
            }
            if (++count == AOF_REWRITE_ITEMS_PER_CMD) count = 0;
            items--;
        }
        quicklistReleaseIterator(li);
    } else {
        serverPanic("Unknown list encoding");
    }
    return 1;
}

/* Emit the commands needed to rebuild a set object.
 * The function returns 0 on error, 1 on success. */
int rewriteSetObject(rio *r, robj *key, robj *o) {
    long long count = 0, items = setTypeSize(o);

    if (o->encoding == OBJ_ENCODING_INTSET) {
        int ii = 0;
        int64_t llval;

        while (intsetGet(o->ptr, ii++, &llval)) {
            if (count == 0) {
                int cmd_items = (items > AOF_REWRITE_ITEMS_PER_CMD) ?
                                AOF_REWRITE_ITEMS_PER_CMD : items;

                if (rioWriteBulkCount(r, '*', 2 + cmd_items) == 0) return 0;
                if (rioWriteBulkString(r, "SADD", 4) == 0) return 0;
                if (rioWriteBulkObject(r, key) == 0) return 0;
            }
            if (rioWriteBulkLongLong(r, llval) == 0) return 0;
            if (++count == AOF_REWRITE_ITEMS_PER_CMD) count = 0;
            items--;
        }
    } else if (o->encoding == OBJ_ENCODING_HT) {
        dictIterator *di = dictGetIterator(o->ptr);
        dictEntry *de;

        while ((de = dictNext(di)) != NULL) {
            sds ele = dictGetKey(de);
            if (count == 0) {
                int cmd_items = (items > AOF_REWRITE_ITEMS_PER_CMD) ?
                                AOF_REWRITE_ITEMS_PER_CMD : items;

                if (rioWriteBulkCount(r, '*', 2 + cmd_items) == 0) return 0;
                if (rioWriteBulkString(r, "SADD", 4) == 0) return 0;
                if (rioWriteBulkObject(r, key) == 0) return 0;
            }
            if (rioWriteBulkString(r, ele, sdslen(ele)) == 0) return 0;
            if (++count == AOF_REWRITE_ITEMS_PER_CMD) count = 0;
            items--;
        }
        dictReleaseIterator(di);
    } else {
        serverPanic("Unknown set encoding");
    }
    return 1;
}

/* Emit the commands needed to rebuild a sorted set object.
 * The function returns 0 on error, 1 on success. */
int rewriteSortedSetObject(rio *r, robj *key, robj *o) {
    long long count = 0, items = zsetLength(o);

    if (o->encoding == OBJ_ENCODING_ZIPLIST) {
        unsigned char *zl = o->ptr;
        unsigned char *eptr, *sptr;
        unsigned char *vstr;
        unsigned int vlen;
        long long vll;
        double score;

        eptr = ziplistIndex(zl, 0);
        serverAssert(eptr != NULL);
        sptr = ziplistNext(zl, eptr);
        serverAssert(sptr != NULL);

        while (eptr != NULL) {
            serverAssert(ziplistGet(eptr, &vstr, &vlen, &vll));
            score = zzlGetScore(sptr);

            if (count == 0) {
                int cmd_items = (items > AOF_REWRITE_ITEMS_PER_CMD) ?
                                AOF_REWRITE_ITEMS_PER_CMD : items;

                if (rioWriteBulkCount(r, '*', 2 + cmd_items * 2) == 0) return 0;
                if (rioWriteBulkString(r, "ZADD", 4) == 0) return 0;
                if (rioWriteBulkObject(r, key) == 0) return 0;
            }
            if (rioWriteBulkDouble(r, score) == 0) return 0;
            if (vstr != NULL) {
                if (rioWriteBulkString(r, (char *) vstr, vlen) == 0) return 0;
            } else {
                if (rioWriteBulkLongLong(r, vll) == 0) return 0;
            }
            zzlNext(zl, &eptr, &sptr);
            if (++count == AOF_REWRITE_ITEMS_PER_CMD) count = 0;
            items--;
        }
    } else if (o->encoding == OBJ_ENCODING_SKIPLIST) {
        zset *zs = o->ptr;
        dictIterator *di = dictGetIterator(zs->dict);
        dictEntry *de;

        while ((de = dictNext(di)) != NULL) {
            sds ele = dictGetKey(de);
            double *score = dictGetVal(de);

            if (count == 0) {
                int cmd_items = (items > AOF_REWRITE_ITEMS_PER_CMD) ?
                                AOF_REWRITE_ITEMS_PER_CMD : items;

                if (rioWriteBulkCount(r, '*', 2 + cmd_items * 2) == 0) return 0;
                if (rioWriteBulkString(r, "ZADD", 4) == 0) return 0;
                if (rioWriteBulkObject(r, key) == 0) return 0;
            }
            if (rioWriteBulkDouble(r, *score) == 0) return 0;
            if (rioWriteBulkString(r, ele, sdslen(ele)) == 0) return 0;
            if (++count == AOF_REWRITE_ITEMS_PER_CMD) count = 0;
            items--;
        }
        dictReleaseIterator(di);
    } else {
        serverPanic("Unknown sorted zset encoding");
    }
    return 1;
}

/* Write either the key or the value of the currently selected item of a hash.
 * The 'hi' argument passes a valid Redis hash iterator.
 * The 'what' filed specifies if to write a key or a value and can be
 * either OBJ_HASH_KEY or OBJ_HASH_VALUE.
 *
 * The function returns 0 on error, non-zero on success. */
static int rioWriteHashIteratorCursor(rio *r, hashTypeIterator *hi, int what) {
    if (hi->encoding == OBJ_ENCODING_ZIPLIST) {
        unsigned char *vstr = NULL;
        unsigned int vlen = UINT_MAX;
        long long vll = LLONG_MAX;

        hashTypeCurrentFromZiplist(hi, what, &vstr, &vlen, &vll);
        if (vstr)
            return rioWriteBulkString(r, (char *) vstr, vlen);
        else
            return rioWriteBulkLongLong(r, vll);
    } else if (hi->encoding == OBJ_ENCODING_HT) {
        sds value = hashTypeCurrentFromHashTable(hi, what);
        return rioWriteBulkString(r, value, sdslen(value));
    }

    serverPanic("Unknown hash encoding");
    return 0;
}

/* Emit the commands needed to rebuild a hash object.
 * The function returns 0 on error, 1 on success. */
int rewriteHashObject(rio *r, robj *key, robj *o) {
    hashTypeIterator *hi;
    long long count = 0, items = hashTypeLength(o);

    hi = hashTypeInitIterator(o);
    while (hashTypeNext(hi) != C_ERR) {
        if (count == 0) {
            int cmd_items = (items > AOF_REWRITE_ITEMS_PER_CMD) ?
                            AOF_REWRITE_ITEMS_PER_CMD : items;

            if (rioWriteBulkCount(r, '*', 2 + cmd_items * 2) == 0) return 0;
            if (rioWriteBulkString(r, "HMSET", 5) == 0) return 0;
            if (rioWriteBulkObject(r, key) == 0) return 0;
        }

        if (rioWriteHashIteratorCursor(r, hi, OBJ_HASH_KEY) == 0) return 0;
        if (rioWriteHashIteratorCursor(r, hi, OBJ_HASH_VALUE) == 0) return 0;
        if (++count == AOF_REWRITE_ITEMS_PER_CMD) count = 0;
        items--;
    }

    hashTypeReleaseIterator(hi);

    return 1;
}

/* Helper for rewriteStreamObject() that generates a bulk string into the
 * AOF representing the ID 'id'. */
int rioWriteBulkStreamID(rio *r, streamID *id) {
    int retval;

    sds replyid = sdscatfmt(sdsempty(), "%U-%U", id->ms, id->seq);
    retval = rioWriteBulkString(r, replyid, sdslen(replyid));
    sdsfree(replyid);
    return retval;
}

/* Helper for rewriteStreamObject(): emit the XCLAIM needed in order to
 * add the message described by 'nack' having the id 'rawid', into the pending
 * list of the specified consumer. All this in the context of the specified
 * key and group. */
int rioWriteStreamPendingEntry(rio *r, robj *key, const char *groupname, size_t groupname_len, streamConsumer *consumer,
                               unsigned char *rawid, streamNACK *nack) {
    /* XCLAIM <key> <group> <consumer> 0 <id> TIME <milliseconds-unix-time>
              RETRYCOUNT <count> JUSTID FORCE. */
    streamID id;
    streamDecodeID(rawid, &id);
    if (rioWriteBulkCount(r, '*', 12) == 0) return 0;
    if (rioWriteBulkString(r, "XCLAIM", 6) == 0) return 0;
    if (rioWriteBulkObject(r, key) == 0) return 0;
    if (rioWriteBulkString(r, groupname, groupname_len) == 0) return 0;
    if (rioWriteBulkString(r, consumer->name, sdslen(consumer->name)) == 0) return 0;
    if (rioWriteBulkString(r, "0", 1) == 0) return 0;
    if (rioWriteBulkStreamID(r, &id) == 0) return 0;
    if (rioWriteBulkString(r, "TIME", 4) == 0) return 0;
    if (rioWriteBulkLongLong(r, nack->delivery_time) == 0) return 0;
    if (rioWriteBulkString(r, "RETRYCOUNT", 10) == 0) return 0;
    if (rioWriteBulkLongLong(r, nack->delivery_count) == 0) return 0;
    if (rioWriteBulkString(r, "JUSTID", 6) == 0) return 0;
    if (rioWriteBulkString(r, "FORCE", 5) == 0) return 0;
    return 1;
}

/* Emit the commands needed to rebuild a stream object.
 * The function returns 0 on error, 1 on success. */
int rewriteStreamObject(rio *r, robj *key, robj *o) {
    stream *s = o->ptr;
    streamIterator si;
    streamIteratorStart(&si, s, NULL, NULL, 0);
    streamID id;
    int64_t numfields;

    if (s->length) {
        /* Reconstruct the stream data using XADD commands. */
        while (streamIteratorGetID(&si, &id, &numfields)) {
            /* Emit a two elements array for each item. The first is
             * the ID, the second is an array of field-value pairs. */

            /* Emit the XADD <key> <id> ...fields... command. */
            if (rioWriteBulkCount(r, '*', 3 + numfields * 2) == 0) return 0;
            if (rioWriteBulkString(r, "XADD", 4) == 0) return 0;
            if (rioWriteBulkObject(r, key) == 0) return 0;
            if (rioWriteBulkStreamID(r, &id) == 0) return 0;
            while (numfields--) {
                unsigned char *field, *value;
                int64_t field_len, value_len;
                streamIteratorGetField(&si, &field, &value, &field_len, &value_len);
                if (rioWriteBulkString(r, (char *) field, field_len) == 0) return 0;
                if (rioWriteBulkString(r, (char *) value, value_len) == 0) return 0;
            }
        }
    } else {
        /* Use the XADD MAXLEN 0 trick to generate an empty stream if
         * the key we are serializing is an empty string, which is possible
         * for the Stream type. */
        if (rioWriteBulkCount(r, '*', 7) == 0) return 0;
        if (rioWriteBulkString(r, "XADD", 4) == 0) return 0;
        if (rioWriteBulkObject(r, key) == 0) return 0;
        if (rioWriteBulkString(r, "MAXLEN", 6) == 0) return 0;
        if (rioWriteBulkString(r, "0", 1) == 0) return 0;
        if (rioWriteBulkStreamID(r, &s->last_id) == 0) return 0;
        if (rioWriteBulkString(r, "x", 1) == 0) return 0;
        if (rioWriteBulkString(r, "y", 1) == 0) return 0;
    }

    /* Append XSETID after XADD, make sure lastid is correct,
     * in case of XDEL lastid. */
    if (rioWriteBulkCount(r, '*', 3) == 0) return 0;
    if (rioWriteBulkString(r, "XSETID", 6) == 0) return 0;
    if (rioWriteBulkObject(r, key) == 0) return 0;
    if (rioWriteBulkStreamID(r, &s->last_id) == 0) return 0;


    /* Create all the stream consumer groups. */
    if (s->cgroups) {
        raxIterator ri;
        raxStart(&ri, s->cgroups);
        raxSeek(&ri, "^", NULL, 0);
        while (raxNext(&ri)) {
            streamCG *group = ri.data;
            /* Emit the XGROUP CREATE in order to create the group. */
            if (rioWriteBulkCount(r, '*', 5) == 0) return 0;
            if (rioWriteBulkString(r, "XGROUP", 6) == 0) return 0;
            if (rioWriteBulkString(r, "CREATE", 6) == 0) return 0;
            if (rioWriteBulkObject(r, key) == 0) return 0;
            if (rioWriteBulkString(r, (char *) ri.key, ri.key_len) == 0) return 0;
            if (rioWriteBulkStreamID(r, &group->last_id) == 0) return 0;

            /* Generate XCLAIMs for each consumer that happens to
             * have pending entries. Empty consumers have no semantical
             * value so they are discarded. */
            raxIterator ri_cons;
            raxStart(&ri_cons, group->consumers);
            raxSeek(&ri_cons, "^", NULL, 0);
            while (raxNext(&ri_cons)) {
                streamConsumer *consumer = ri_cons.data;
                /* For the current consumer, iterate all the PEL entries
                 * to emit the XCLAIM protocol. */
                raxIterator ri_pel;
                raxStart(&ri_pel, consumer->pel);
                raxSeek(&ri_pel, "^", NULL, 0);
                while (raxNext(&ri_pel)) {
                    streamNACK *nack = ri_pel.data;
                    if (rioWriteStreamPendingEntry(r, key, (char *) ri.key,
                                                   ri.key_len, consumer,
                                                   ri_pel.key, nack) == 0) {
                        return 0;
                    }
                }
                raxStop(&ri_pel);
            }
            raxStop(&ri_cons);
        }
        raxStop(&ri);
    }

    streamIteratorStop(&si);
    return 1;
}

/* Call the module type callback in order to rewrite a data type
 * that is exported by a module and is not handled by Redis itself.
 * The function returns 0 on error, 1 on success. */
int rewriteModuleObject(rio *r, robj *key, robj *o) {
    RedisModuleIO io;
    moduleValue *mv = o->ptr;
    moduleType *mt = mv->type;
    moduleInitIOContext(io, mt, r, key);
    mt->aof_rewrite(&io, key, mv->value);
    if (io.ctx) {
        moduleFreeContext(io.ctx);
        zfree(io.ctx);
    }
    return io.error ? 0 : 1;
}

/* 读取父进程和子进程间的操作命令传输管道中的数据*/
ssize_t aofReadDiffFromParent(void) {
    char buf[65536]; /* 64KB缓冲区 */
    ssize_t nread, total = 0;
    //从aof_pipe_read_data_from_parent管道读取数据
    while ((nread = read(server.aof_pipe_read_data_from_parent, buf, sizeof(buf))) > 0) {
        server.aof_child_diff = sdscatlen(server.aof_child_diff, buf, nread);
        total += nread;
    }
    return total;
}

//aof文件重写
int rewriteAppendOnlyFileRio(rio *aof) {
    dictIterator *di = NULL;
    dictEntry *de;
    size_t processed = 0;
    int j;

    for (j = 0; j < server.dbnum; j++) {
        char selectcmd[] = "*2\r\n$6\r\nSELECT\r\n"; //select db
        redisDb *db = server.db + j;
        dict *d = db->dict;
        if (dictSize(d) == 0) continue; //忽略空数据库
        di = dictGetSafeIterator(d);

        /* SELECT the new DB */
        if (rioWrite(aof, selectcmd, sizeof(selectcmd) - 1) == 0) goto werr;
        if (rioWriteBulkLongLong(aof, j) == 0) goto werr;

        /* 遍历数据库中的所有键 */
        while ((de = dictNext(di)) != NULL) {
            sds keystr;
            robj key, *o;
            long long expiretime;

            keystr = dictGetKey(de);
            o = dictGetVal(de);
            initStaticStringObject(key, keystr);

            expiretime = getExpire(db, &key); //获取过期时间

            /* 根据键的类型对键进行重写 */
            if (o->type == OBJ_STRING) {
                /* Emit a SET command */
                char cmd[] = "*3\r\n$3\r\nSET\r\n";
                if (rioWrite(aof, cmd, sizeof(cmd) - 1) == 0) goto werr;
                /* Key and value */
                if (rioWriteBulkObject(aof, &key) == 0) goto werr;
                if (rioWriteBulkObject(aof, o) == 0) goto werr;
            } else if (o->type == OBJ_LIST) {
                if (rewriteListObject(aof, &key, o) == 0) goto werr;
            } else if (o->type == OBJ_SET) {
                if (rewriteSetObject(aof, &key, o) == 0) goto werr;
            } else if (o->type == OBJ_ZSET) {
                if (rewriteSortedSetObject(aof, &key, o) == 0) goto werr;
            } else if (o->type == OBJ_HASH) {
                if (rewriteHashObject(aof, &key, o) == 0) goto werr;
            } else if (o->type == OBJ_STREAM) {
                if (rewriteStreamObject(aof, &key, o) == 0) goto werr;
            } else if (o->type == OBJ_MODULE) {
                if (rewriteModuleObject(aof, &key, o) == 0) goto werr;
            } else {
                serverPanic("Unknown object type");
            }
            /* Save the expire time */
            if (expiretime != -1) {
                char cmd[] = "*3\r\n$9\r\nPEXPIREAT\r\n";
                if (rioWrite(aof, cmd, sizeof(cmd) - 1) == 0) goto werr;
                if (rioWriteBulkObject(aof, &key) == 0) goto werr;
                if (rioWriteBulkLongLong(aof, expiretime) == 0) goto werr;
            }
            /* Read some diff from the parent process from time to time. */
            if (aof->processed_bytes > processed + AOF_READ_DIFF_INTERVAL_BYTES) {
                processed = aof->processed_bytes;
                aofReadDiffFromParent();
            }
        }
        dictReleaseIterator(di);
        di = NULL;
    }
    return C_OK;

    werr:
    if (di) dictReleaseIterator(di);
    return C_ERR;
}

/* Write a sequence of commands able to fully rebuild the dataset into
 * "filename". Used both by REWRITEAOF and BGREWRITEAOF.
 *
 * In order to minimize the number of commands needed in the rewritten
 * log Redis uses variadic commands when possible, such as RPUSH, SADD
 * and ZADD. However at max AOF_REWRITE_ITEMS_PER_CMD items per time
 * are inserted using a single command.
 * 重写aof
 * */
int rewriteAppendOnlyFile(char *filename) {
    rio aof;
    FILE *fp;
    char tmpfile[256];
    char byte;

    snprintf(tmpfile, 256, "temp-rewriteaof-%d.aof", (int) getpid());
    fp = fopen(tmpfile, "w");
    if (!fp) {
        serverLog(LL_WARNING, "Opening the temp file for AOF rewrite in rewriteAppendOnlyFile(): %s", strerror(errno));
        return C_ERR;
    }

    server.aof_child_diff = sdsempty();
    rioInitWithFile(&aof, fp); //创建一个新的aof文件

    if (server.aof_rewrite_incremental_fsync)
        rioSetAutoSync(&aof, REDIS_AUTOSYNC_BYTES);
    /*
     * aof_use_rdb_preamble是一个Redis配置参数,用于控制AOF文件的格式。
     * 当参数值为yes时,在AOF重写时,新AOF会使用RDB格式的文件头。
     * 之后的数据部分使用常规的AOF格式,即Redis命令的文本表示。
     * */
    if (server.aof_use_rdb_preamble) {
        int error;
        if (rdbSaveRio(&aof, &error, RDB_SAVE_AOF_PREAMBLE, NULL) == C_ERR) {
            errno = error;
            goto werr;
        }
    } else {
        if (rewriteAppendOnlyFileRio(&aof) == C_ERR) goto werr;
    }

    /* Do an initial slow fsync here while the parent is still sending
     * data, in order to make the next final fsync faster. */
    if (fflush(fp) == EOF) goto werr;
    if (fsync(fileno(fp)) == -1) goto werr;

    /* Read again a few times to get more data from the parent.
     * We can't read forever (the server may receive data from clients
     * faster than it is able to send data to the child), so we try to read
     * some more data in a loop as soon as there is a good chance more data
     * will come. If it looks like we are wasting time, we abort (this
     * happens after 20 ms without new data). */
    int nodata = 0;
    mstime_t start = mstime();
    while (mstime() - start < 1000 && nodata < 20) {
        if (aeWait(server.aof_pipe_read_data_from_parent, AE_READABLE, 1) <= 0) {
            nodata++;
            continue;
        }
        nodata = 0; /* Start counting from zero, we stop on N *contiguous*
                       timeouts. */
        aofReadDiffFromParent();
    }

    /* 让主进程停止发送新写操作 */
    if (write(server.aof_pipe_write_ack_to_parent, "!", 1) != 1) goto werr;
    if (anetNonBlock(NULL, server.aof_pipe_read_ack_from_parent) != ANET_OK)
        goto werr;
    //从aof_pipe_read_ack_from_parent管道读取主进程发送的ACK信息
    if (syncRead(server.aof_pipe_read_ack_from_parent, &byte, 1, 5000) != 1 ||
        byte != '!')
        goto werr;
    serverLog(LL_NOTICE, "Parent agreed to stop sending diffs. Finalizing AOF...");

    /* Read the final diff if any. */
    aofReadDiffFromParent();

    serverLog(LL_NOTICE,
              "Concatenating %.2f MB of AOF diff received from parent.",
              (double) sdslen(server.aof_child_diff) / (1024 * 1024));
    //将aof_child_diff中累积的操作命令写入AOF重写日志
    if (rioWrite(&aof, server.aof_child_diff, sdslen(server.aof_child_diff)) == 0)
        goto werr;

    /* Make sure data will not remain on the OS's output buffers */
    if (fflush(fp) == EOF) goto werr;
    if (fsync(fileno(fp)) == -1) goto werr;
    if (fclose(fp) == EOF) goto werr;

    /* rename功能等同于Unix中的mv命令 */
    if (rename(tmpfile, filename) == -1) {
        serverLog(LL_WARNING, "Error moving temp append only file on the final destination: %s", strerror(errno));
        unlink(tmpfile);
        return C_ERR;
    }
    serverLog(LL_NOTICE, "SYNC append only file rewrite performed");
    return C_OK;

    werr:
    serverLog(LL_WARNING, "Write error writing append only file on disk: %s", strerror(errno));
    fclose(fp);
    unlink(tmpfile);
    return C_ERR;
}

/* ----------------------------------------------------------------------------
 * AOF rewrite pipes for IPC
 * -------------------------------------------------------------------------- */

/* 收到子进程发送的!, 表示主进程收到了重写子进程发送的ACK,
 * 主进程往aof_pipe_write_ack_to_child管道写入!, 同时给子进程回复一个ACK
 * */
void aofChildPipeReadable(aeEventLoop *el, int fd, void *privdata, int mask) {
    char byte;
    UNUSED(el);
    UNUSED(privdata);
    UNUSED(mask);

    if (read(fd, &byte, 1) == 1 && byte == '!') {
        serverLog(LL_NOTICE, "AOF rewrite child asks to stop sending diffs.");
        server.aof_stop_sending_diff = 1;
        if (write(server.aof_pipe_write_ack_to_child, "!", 1) != 1) {
            /* If we can't send the ack, inform the user, but don't try again
             * since in the other side the children will use a timeout if the
             * kernel can't buffer our write, or, the children was
             * terminated. */
            serverLog(LL_WARNING, "Can't send ACK to AOF child: %s",
                      strerror(errno));
        }
    }
    /* Remove the handler since this can be called only one time during a
     * rewrite. */
    aeDeleteFileEvent(server.el, server.aof_pipe_read_ack_from_child, AE_READABLE);
}

/* 创建三个管道，用于aof重写时使用
 * 1： 父进程将增量数据发给子进程 0读1写
 * 2： 子进程通知父进程重写done
 * 3： 父进程通知子进程收到了done
 * */
int aofCreatePipes(void) {
    int fds[6] = {-1, -1, -1, -1, -1, -1};
    int j;

    if (pipe(fds) == -1) goto error; /* parent -> children data. */
    if (pipe(fds + 2) == -1) goto error; /* children -> parent ack. */
    if (pipe(fds + 4) == -1) goto error; /* parent -> children ack. */
    /* 将第一个和第二个文件描述符设置为非阻塞 */
    if (anetNonBlock(NULL, fds[0]) != ANET_OK) goto error;
    if (anetNonBlock(NULL, fds[1]) != ANET_OK) goto error;
    //在第三个描述符注册读事件监听 aof_pipe_write_ack_to_parent
    if (aeCreateFileEvent(server.el, fds[2], AE_READABLE, aofChildPipeReadable, NULL) == AE_ERR) goto error;

    server.aof_pipe_write_data_to_child = fds[1];
    server.aof_pipe_read_data_from_parent = fds[0];
    server.aof_pipe_write_ack_to_parent = fds[3];
    server.aof_pipe_read_ack_from_child = fds[2];
    server.aof_pipe_write_ack_to_child = fds[5];
    server.aof_pipe_read_ack_from_parent = fds[4];
    server.aof_stop_sending_diff = 0;
    return C_OK;

    error:
    serverLog(LL_WARNING, "Error opening /setting AOF rewrite IPC pipes: %s",
              strerror(errno));
    for (j = 0; j < 6; j++) if (fds[j] != -1) close(fds[j]);
    return C_ERR;
}

void aofClosePipes(void) {
    aeDeleteFileEvent(server.el, server.aof_pipe_read_ack_from_child, AE_READABLE);
    aeDeleteFileEvent(server.el, server.aof_pipe_write_data_to_child, AE_WRITABLE);
    close(server.aof_pipe_write_data_to_child);
    close(server.aof_pipe_read_data_from_parent);
    close(server.aof_pipe_write_ack_to_parent);
    close(server.aof_pipe_read_ack_from_child);
    close(server.aof_pipe_write_ack_to_child);
    close(server.aof_pipe_read_ack_from_parent);
}

/* ----------------------------------------------------------------------------
 * AOF background rewrite
 * ------------------------------------------------------------------------- */

/* aof重写:
 *
 * 1) 调用 BGREWRITEAOF命令
 * 2) fork创建一个重写子进程:
 *    2a) 子进程重写aof到一个临时文件.
 *    2b) 父进程在 server.aof_rewrite_buf 中记录新产生的log。
 * 3) 子进程完成后，退出.
 * 4) 父进程将捕获退出代码，然后将 server.aof_rewrite_buf 中累积的数据追加到临时文件中，最后以实际文件名重命名(2) 临时文件。
 *    产生的临时文件替换原来的aof文件，perfect
 */
int rewriteAppendOnlyFileBackground(void) {
    pid_t childpid;
    long long start;

    if (server.aof_child_pid != -1 || server.rdb_child_pid != -1) return C_ERR;
    if (aofCreatePipes() != C_OK) return C_ERR;
    openChildInfoPipe();
    start = ustime();
    if ((childpid = fork()) == 0) {
        char tmpfile[256];

        /* Child */
        closeClildUnusedResourceAfterFork();
        redisSetProcTitle("redis-aof-rewrite");
        //创建一个临时aof文件
        snprintf(tmpfile, 256, "temp-rewriteaof-bg-%d.aof", (int) getpid());
        if (rewriteAppendOnlyFile(tmpfile) == C_OK) {
            size_t private_dirty = zmalloc_get_private_dirty(-1);

            if (private_dirty) {
                serverLog(LL_NOTICE,
                          "AOF rewrite: %zu MB of memory used by copy-on-write",
                          private_dirty / (1024 * 1024));
            }

            server.child_info_data.cow_size = private_dirty;
            sendChildInfo(CHILD_INFO_TYPE_AOF);
            exitFromChild(0);
        } else {
            exitFromChild(1);
        }
    } else {
        /* Parent */
        server.stat_fork_time = ustime() - start;
        server.stat_fork_rate = (double) zmalloc_used_memory() * 1000000 / server.stat_fork_time /
                                (1024 * 1024 * 1024); /* GB per second. */
        latencyAddSampleIfNeeded("fork", server.stat_fork_time / 1000);
        if (childpid == -1) {
            closeChildInfoPipe();
            serverLog(LL_WARNING,
                      "Can't rewrite append only file in background: fork: %s",
                      strerror(errno));
            aofClosePipes();
            return C_ERR;
        }
        serverLog(LL_NOTICE,
                  "Background append only file rewriting started by pid %d", childpid);
        server.aof_rewrite_scheduled = 0;
        server.aof_rewrite_time_start = time(NULL);
        server.aof_child_pid = childpid; //记录重写子进程的pid
        updateDictResizePolicy();//关闭rehash功能
        /* We set appendseldb to -1 in order to force the next call to the
         * feedAppendOnlyFile() to issue a SELECT command, so the differences
         * accumulated by the parent into server.aof_rewrite_buf will start
         * with a SELECT statement and it will be safe to merge. */
        server.aof_selected_db = -1;
        replicationScriptCacheFlush();
        return C_OK;
    }
    return C_OK; /* unreached */
}

void bgrewriteaofCommand(client *c) {
    //aof重写子进程正在运行?
    if (server.aof_child_pid != -1) {
        addReplyError(c, "Background append only file rewriting already in progress");
    } else if (server.rdb_child_pid != -1) {
        //是否有创建rdb的子进程正在执行
        server.aof_rewrite_scheduled = 1;
        addReplyStatus(c, "Background append only file rewriting scheduled");
    } else if (rewriteAppendOnlyFileBackground() == C_OK) {
        addReplyStatus(c, "Background append only file rewriting started");
    } else {
        addReply(c, shared.err);
    }
}

void aofRemoveTempFile(pid_t childpid) {
    char tmpfile[256];

    snprintf(tmpfile, 256, "temp-rewriteaof-bg-%d.aof", (int) childpid);
    unlink(tmpfile);
}

/* Update the server.aof_current_size field explicitly using stat(2)
 * to check the size of the file. This is useful after a rewrite or after
 * a restart, normally the size is updated just adding the write length
 * to the current length, that is much faster. */
void aofUpdateCurrentSize(void) {
    struct redis_stat sb;
    mstime_t latency;

    latencyStartMonitor(latency);
    if (redis_fstat(server.aof_fd, &sb) == -1) {
        serverLog(LL_WARNING, "Unable to obtain the AOF file length. stat: %s",
                  strerror(errno));
    } else {
        server.aof_current_size = sb.st_size;
    }
    latencyEndMonitor(latency);
    latencyAddSampleIfNeeded("aof-fstat", latency);
}

/* A background append only file rewriting (BGREWRITEAOF) terminated its work.
 * Handle this. */
void backgroundRewriteDoneHandler(int exitcode, int bysignal) {
    if (!bysignal && exitcode == 0) {
        int newfd, oldfd;
        char tmpfile[256];
        long long now = ustime();
        mstime_t latency;

        serverLog(LL_NOTICE,
                  "Background AOF rewrite terminated with success");

        /* Flush the differences accumulated by the parent to the
         * rewritten AOF. */
        latencyStartMonitor(latency);
        snprintf(tmpfile, 256, "temp-rewriteaof-bg-%d.aof",
                 (int) server.aof_child_pid);
        newfd = open(tmpfile, O_WRONLY | O_APPEND);
        if (newfd == -1) {
            serverLog(LL_WARNING,
                      "Unable to open the temporary AOF produced by the child: %s", strerror(errno));
            goto cleanup;
        }

        if (aofRewriteBufferWrite(newfd) == -1) {
            serverLog(LL_WARNING,
                      "Error trying to flush the parent diff to the rewritten AOF: %s", strerror(errno));
            close(newfd);
            goto cleanup;
        }
        latencyEndMonitor(latency);
        latencyAddSampleIfNeeded("aof-rewrite-diff-write", latency);

        serverLog(LL_NOTICE,
                  "Residual parent diff successfully flushed to the rewritten AOF (%.2f MB)",
                  (double) aofRewriteBufferSize() / (1024 * 1024));

        /* The only remaining thing to do is to rename the temporary file to
         * the configured file and switch the file descriptor used to do AOF
         * writes. We don't want close(2) or rename(2) calls to block the
         * server on old file deletion.
         *
         * There are two possible scenarios:
         *
         * 1) AOF is DISABLED and this was a one time rewrite. The temporary
         * file will be renamed to the configured file. When this file already
         * exists, it will be unlinked, which may block the server.
         *
         * 2) AOF is ENABLED and the rewritten AOF will immediately start
         * receiving writes. After the temporary file is renamed to the
         * configured file, the original AOF file descriptor will be closed.
         * Since this will be the last reference to that file, closing it
         * causes the underlying file to be unlinked, which may block the
         * server.
         *
         * To mitigate the blocking effect of the unlink operation (either
         * caused by rename(2) in scenario 1, or by close(2) in scenario 2), we
         * use a background thread to take care of this. First, we
         * make scenario 1 identical to scenario 2 by opening the target file
         * when it exists. The unlink operation after the rename(2) will then
         * be executed upon calling close(2) for its descriptor. Everything to
         * guarantee atomicity for this switch has already happened by then, so
         * we don't care what the outcome or duration of that close operation
         * is, as long as the file descriptor is released again. */
        if (server.aof_fd == -1) {
            /* AOF disabled */

            /* Don't care if this fails: oldfd will be -1 and we handle that.
             * One notable case of -1 return is if the old file does
             * not exist. */
            oldfd = open(server.aof_filename, O_RDONLY | O_NONBLOCK);
        } else {
            /* AOF enabled */
            oldfd = -1; /* We'll set this to the current AOF filedes later. */
        }

        /* Rename the temporary file. This will not unlink the target file if
         * it exists, because we reference it with "oldfd". */
        latencyStartMonitor(latency);
        if (rename(tmpfile, server.aof_filename) == -1) {
            serverLog(LL_WARNING,
                      "Error trying to rename the temporary AOF file %s into %s: %s",
                      tmpfile,
                      server.aof_filename,
                      strerror(errno));
            close(newfd);
            if (oldfd != -1) close(oldfd);
            goto cleanup;
        }
        latencyEndMonitor(latency);
        latencyAddSampleIfNeeded("aof-rename", latency);

        if (server.aof_fd == -1) {
            /* AOF disabled, we don't need to set the AOF file descriptor
             * to this new file, so we can close it. */
            close(newfd);
        } else {
            /* AOF enabled, replace the old fd with the new one. */
            oldfd = server.aof_fd;
            server.aof_fd = newfd;
            if (server.aof_fsync == AOF_FSYNC_ALWAYS)
                redis_fsync(newfd);
            else if (server.aof_fsync == AOF_FSYNC_EVERYSEC)
                aof_background_fsync(newfd);
            server.aof_selected_db = -1; /* Make sure SELECT is re-issued */
            aofUpdateCurrentSize();
            server.aof_rewrite_base_size = server.aof_current_size;
            server.aof_fsync_offset = server.aof_current_size;

            /* Clear regular AOF buffer since its contents was just written to
             * the new AOF from the background rewrite buffer. */
            sdsfree(server.aof_buf);
            server.aof_buf = sdsempty();
        }

        server.aof_lastbgrewrite_status = C_OK;

        serverLog(LL_NOTICE, "Background AOF rewrite finished successfully");
        /* Change state from WAIT_REWRITE to ON if needed */
        if (server.aof_state == AOF_WAIT_REWRITE)
            server.aof_state = AOF_ON;

        /* Asynchronously close the overwritten AOF. */
        if (oldfd != -1) bioCreateBackgroundJob(BIO_CLOSE_FILE, (void *) (long) oldfd, NULL, NULL);

        serverLog(LL_VERBOSE,
                  "Background AOF rewrite signal handler took %lldus", ustime() - now);
    } else if (!bysignal && exitcode != 0) {
        server.aof_lastbgrewrite_status = C_ERR;

        serverLog(LL_WARNING,
                  "Background AOF rewrite terminated with error");
    } else {
        /* SIGUSR1 is whitelisted, so we have a way to kill a child without
         * tirggering an error condition. */
        if (bysignal != SIGUSR1)
            server.aof_lastbgrewrite_status = C_ERR;

        serverLog(LL_WARNING,
                  "Background AOF rewrite terminated by signal %d", bysignal);
    }

    cleanup:
    aofClosePipes();
    aofRewriteBufferReset();
    aofRemoveTempFile(server.aof_child_pid);
    server.aof_child_pid = -1;
    server.aof_rewrite_time_last = time(NULL) - server.aof_rewrite_time_start;
    server.aof_rewrite_time_start = -1;
    /* Schedule a new rewrite if we are waiting for it to switch the AOF ON. */
    if (server.aof_state == AOF_WAIT_REWRITE)
        server.aof_rewrite_scheduled = 1;
}
