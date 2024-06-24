/*
 * MULTI: 开启一个事务,后续命令都会被放入事务命令队列
 * EXEC: 可以执行事务命令队列中的所有命令
 * DISCARD: 抛弃事务命令队列中的命令. 和EXEC都可以结束当前事务.
 * WATCH: 监视指定键,当后续事务执行前发现这些键已修改时,拒绝执行事务.
 * */
#include "server.h"

/* ================================ MULTI/EXEC ============================== */

/* 初始化client事务上下文--- MULTI/EXEC */
void initClientMultiState(client *c) {
    c->mstate.commands = NULL;
    c->mstate.count = 0;
    c->mstate.cmd_flags = 0;
}

/* Release all the resources associated with MULTI/EXEC state */
void freeClientMultiState(client *c) {
    int j;

    for (j = 0; j < c->mstate.count; j++) {
        int i;
        multiCmd *mc = c->mstate.commands + j;

        for (i = 0; i < mc->argc; i++)
            decrRefCount(mc->argv[i]);
        zfree(mc->argv);
    }
    zfree(c->mstate.commands);
}

/* 将命令请求添加到客户端事务命令队列client->mstate.commands中 */
void queueMultiCommand(client *c) {
    multiCmd *mc;
    int j;

    c->mstate.commands = zrealloc(c->mstate.commands,
                                  sizeof(multiCmd) * (c->mstate.count + 1));
    mc = c->mstate.commands + c->mstate.count;
    mc->cmd = c->cmd;
    mc->argc = c->argc;
    mc->argv = zmalloc(sizeof(robj *) * c->argc);
    memcpy(mc->argv, c->argv, sizeof(robj *) * c->argc);
    for (j = 0; j < c->argc; j++)
        incrRefCount(mc->argv[j]);
    c->mstate.count++;
    c->mstate.cmd_flags |= c->cmd->flags;
}

/*
 * 放弃事务的执行
 * 清空当前 client 之前缓存的命令，并对事务中的 key 执行 unWatch 操作，
 * 最后重置 client 的事务标记
*/
void discardTransaction(client *c) {
    freeClientMultiState(c);
    initClientMultiState(c);
    c->flags &= ~(CLIENT_MULTI | CLIENT_DIRTY_CAS | CLIENT_DIRTY_EXEC);
    unwatchAllKeys(c);
}

/* Flag the transacation as DIRTY_EXEC so that EXEC will fail.
 * Should be called every time there is an error while queueing a command. */
void flagTransaction(client *c) {
    if (c->flags & CLIENT_MULTI)
        c->flags |= CLIENT_DIRTY_EXEC;
}

// MULTI命令处理
void multiCommand(client *c) {
    if (c->flags & CLIENT_MULTI) {
        addReplyError(c, "MULTI calls can not be nested");
        return;
    }
    // 给客户端打开CLIENT_MULTI标识,代表该客户端已开启事务.
    c->flags |= CLIENT_MULTI;
    addReply(c, shared.ok);
}

// 放弃事务命令队列中的命令
void discardCommand(client *c) {
    if (!(c->flags & CLIENT_MULTI)) {
        addReplyError(c, "DISCARD without MULTI");
        return;
    }
    discardTransaction(c);
    addReply(c, shared.ok);
}

/* Send a MULTI command to all the slaves and AOF file. Check the execCommand
 * implementation for more information. */
void execCommandPropagateMulti(client *c) {
    robj *multistring = createStringObject("MULTI", 5);

    propagate(server.multiCommand, c->db->id, &multistring, 1,
              PROPAGATE_AOF | PROPAGATE_REPL);
    decrRefCount(multistring);
}

// 处理EXEC
void execCommand(client *c) {
    int j;
    robj **orig_argv;
    int orig_argc;
    struct redisCommand *orig_cmd;
    int must_propagate = 0; /* Need to propagate MULTI/EXEC to AOF / slaves? */
    int was_master = server.masterhost == NULL;

    // 如果当前不在事务中
    if (!(c->flags & CLIENT_MULTI)) {
        addReplyError(c, "EXEC without MULTI");
        return;
    }

    /* 当客户端监视的键被修改(CLIENT_DIRTY_CAS标志),
     * 或者已拒绝事务中的命令(CLIENT_DIRTY_EXEC)时,
     * 直接抛弃事务命令队列中的命令,并进行错误处理.
     * */
    if (c->flags & (CLIENT_DIRTY_CAS | CLIENT_DIRTY_EXEC)) {
        addReply(c, c->flags & CLIENT_DIRTY_EXEC ? shared.execaborterr :
                    shared.nullmultibulk);
        discardTransaction(c);
        goto handle_monitor;
    }

    /* 如果事务内有写入命令，并且这是一个只读slave，我们希望发送错误。
     * 当实例是主实例或可写副本时启动事务，然后配置发生更改（例如，实例变成副本）时，就会发生这种情况。 */
    if (!server.loading && server.masterhost && server.repl_slave_ro &&
        !(c->flags & CLIENT_MASTER) && c->mstate.cmd_flags & CMD_WRITE) {
        addReplyError(c,
                      "Transaction contains write commands but instance "
                      "is now a read-only slave. EXEC aborted.");
        discardTransaction(c);
        goto handle_monitor;
    }

    /* Exec all the queued commands */
    unwatchAllKeys(c); /* 取消当前客户端对所有键的监视,所以watch命令只能 作用于后续的一个事务*/
    orig_argv = c->argv;
    orig_argc = c->argc;
    orig_cmd = c->cmd;
    addReplyMultiBulkLen(c, c->mstate.count);
    for (j = 0; j < c->mstate.count; j++) {
        c->argc = c->mstate.commands[j].argc;
        c->argv = c->mstate.commands[j].argv;
        c->cmd = c->mstate.commands[j].cmd;

        /* 在执行事务的第一个写命令之前,传播MULTI命令到AOF和slave.
         * 不带写命令的事务不会传播MULTI命令(不属于写命令)
         * */
        if (!must_propagate && !(c->cmd->flags & (CMD_READONLY | CMD_ADMIN))) {
            execCommandPropagateMulti(c);
            must_propagate = 1;
        }

        call(c, server.loading ? CMD_CALL_NONE : CMD_CALL_FULL);

        /* Commands may alter argc/argv, restore mstate. */
        c->mstate.commands[j].argc = c->argc;
        c->mstate.commands[j].argv = c->argv;
        c->mstate.commands[j].cmd = c->cmd;
    }
    c->argv = orig_argv;
    c->argc = orig_argc;
    c->cmd = orig_cmd;
    // 执行完所有命令,重置客户端事务上下文.代表当前事务已经处理完成
    discardTransaction(c);

    /* 如果事务中执行了写命令 */
    if (must_propagate) {
        int is_master = server.masterhost == NULL;
        server.dirty++;
        /* 如果在 MULTI/EXEC 块内，此实例突然从主服务器切换到从服务器（使用 SLAVEOF 命令），
         * 则初始 MULTI 会传播到复制积压缓冲区中，但其余部分不会。
         * 我们需要确保 EXEC 添加到复制积压缓冲区 */
        if (server.repl_backlog && was_master && !is_master) {
            char *execcmd = "*1\r\n$4\r\nEXEC\r\n";
            feedReplicationBacklog(execcmd, strlen(execcmd));
        }
    }

    handle_monitor:
    /* Send EXEC to clients waiting data from MONITOR. We do it here
     * since the natural order of commands execution is actually:
     * MUTLI, EXEC, ... commands inside transaction ...
     * Instead EXEC is flagged as CMD_SKIP_MONITOR in the command
     * table, and we do it here with correct ordering. */
    if (listLength(server.monitors) && !server.loading)
        replicationFeedMonitors(c, server.monitors, c->db->id, c->argv, c->argc);
}

/* ===================== WATCH (CAS alike for MULTI/EXEC) ===================
 *
 * The implementation uses a per-DB hash table mapping keys to list of clients
 * WATCHing those keys, so that given a key that is going to be modified
 * we can mark all the associated clients as dirty.
 *
 * Also every client contains a list of WATCHed keys so that's possible to
 * un-watch such keys when the client is freed or when UNWATCH is called. */

/* watch key需要知道监视的哪个db以及key */
typedef struct watchedKey {
    robj *key;
    redisDb *db;
} watchedKey;

/* 监视key */
void watchForKey(client *c, robj *key) {
    list *clients = NULL;
    listIter li;
    listNode *ln;
    watchedKey *wk;

    /* 检查client是否已watch了该key */
    listRewind(c->watched_keys, &li);
    while ((ln = listNext(&li))) {
        wk = listNodeValue(ln);
        if (wk->db == c->db && equalStringObjects(key, wk->key))
            return; /* key已经被watch啦 */
    }
    /* 将客户端添加到redisdb.watched_keys字典中该key对应的客户端列表中 */
    clients = dictFetchValue(c->db->watched_keys, key);
    if (!clients) {
        clients = listCreate();
        dictAdd(c->db->watched_keys, key, clients);
        incrRefCount(key);
    }
    listAddNodeTail(clients, c);
    /* Add the new key to the list of keys watched by this client */
    wk = zmalloc(sizeof(*wk));
    wk->key = key;
    wk->db = c->db;
    incrRefCount(key);
    listAddNodeTail(c->watched_keys, wk);
}

/* Unwatch all the keys watched by this client. To clean the EXEC dirty
 * flag is up to the caller. */
void unwatchAllKeys(client *c) {
    listIter li;
    listNode *ln;

    if (listLength(c->watched_keys) == 0) return;
    listRewind(c->watched_keys, &li);
    while ((ln = listNext(&li))) {
        list *clients;
        watchedKey *wk;

        /* Lookup the watched key -> clients list and remove the client
         * from the list */
        wk = listNodeValue(ln);
        clients = dictFetchValue(wk->db->watched_keys, wk->key);
        serverAssertWithInfo(c, NULL, clients != NULL);
        listDelNode(clients, listSearchKey(clients, c));
        /* Kill the entry at all if this was the only client */
        if (listLength(clients) == 0)
            dictDelete(wk->db->watched_keys, wk->key);
        /* Remove this watched key from the client->watched list */
        listDelNode(c->watched_keys, ln);
        decrRefCount(wk->key);
        zfree(wk);
    }
}

/*  WATCH: 监视指定键,当后续事务执行前发现这些键已修改时,拒绝执行事务. */
void touchWatchedKey(redisDb *db, robj *key) {
    list *clients;
    listIter li;
    listNode *ln;
    // 从redisdb的watched_keys中获取所有监视该键的客户端
    if (dictSize(db->watched_keys) == 0) return;
    clients = dictFetchValue(db->watched_keys, key);
    if (!clients) return;

    listRewind(clients, &li);
    while ((ln = listNext(&li))) {
        client *c = listNodeValue(ln);
        // 给这些客户端添加CLIENT_DIRTY_CAS标志, 代表客户端监视的键已被修改.
        c->flags |= CLIENT_DIRTY_CAS;
    }
}

/* On FLUSHDB or FLUSHALL all the watched keys that are present before the
 * flush but will be deleted as effect of the flushing operation should
 * be touched. "dbid" is the DB that's getting the flush. -1 if it is
 * a FLUSHALL operation (all the DBs flushed). */
void touchWatchedKeysOnFlush(int dbid) {
    listIter li1, li2;
    listNode *ln;

    /* For every client, check all the waited keys */
    listRewind(server.clients, &li1);
    while ((ln = listNext(&li1))) {
        client *c = listNodeValue(ln);
        listRewind(c->watched_keys, &li2);
        while ((ln = listNext(&li2))) {
            watchedKey *wk = listNodeValue(ln);

            /* For every watched key matching the specified DB, if the
             * key exists, mark the client as dirty, as the key will be
             * removed. */
            if (dbid == -1 || wk->db->id == dbid) {
                if (dictFind(wk->db->dict, wk->key->ptr) != NULL)
                    c->flags |= CLIENT_DIRTY_CAS;
            }
        }
    }
}

// 处理WATCH命令
void watchCommand(client *c) {
    int j;

    if (c->flags & CLIENT_MULTI) {
        addReplyError(c, "WATCH inside MULTI is not allowed");
        return;
    }
    for (j = 1; j < c->argc; j++)
        watchForKey(c, c->argv[j]);
    addReply(c, shared.ok);
}

void unwatchCommand(client *c) {
    unwatchAllKeys(c);
    c->flags &= (~CLIENT_DIRTY_CAS);
    addReply(c, shared.ok);
}
