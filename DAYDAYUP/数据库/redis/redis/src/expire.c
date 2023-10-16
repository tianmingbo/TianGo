#include "server.h"

/*-----------------------------------------------------------------------------
 * Incremental collection of expired keys.
 *
 * When keys are accessed they are expired on-access. However we need a
 * mechanism in order to ensure keys are eventually removed when expired even
 * if no access is performed on them.
 *----------------------------------------------------------------------------*/

/* Helper function for the activeExpireCycle() function.
 * This function will try to expire the key that is stored in the hash table
 * entry 'de' of the 'expires' hash table of a Redis database.
 *
 * If the key is found to be expired, it is removed from the database and
 * 1 is returned. Otherwise no operation is performed and 0 is returned.
 *
 * When a key is expired, server.stat_expiredkeys is incremented.
 *
 * The parameter 'now' is the current time in milliseconds as is passed
 * to the function to avoid too many gettimeofday() syscalls. */
int activeExpireCycleTryExpire(redisDb *db, dictEntry *de, long long now) {
    long long t = dictGetSignedIntegerVal(de);
    if (now > t) {
        sds key = dictGetKey(de);
        robj *keyobj = createStringObject(key, sdslen(key));

        propagateExpire(db, keyobj, server.lazyfree_lazy_expire);
        if (server.lazyfree_lazy_expire)
            dbAsyncDelete(db, keyobj);
        else
            dbSyncDelete(db, keyobj);
        notifyKeyspaceEvent(NOTIFY_EXPIRED,
                            "expired", keyobj, db->id);
        decrRefCount(keyobj);
        server.stat_expiredkeys++;
        return 1;
    } else {
        return 0;
    }
}

/* 尝试使一些超时的key过期。 使用的算法是自适应的，如果过期key很少，则将使用很少的 CPU 周期.
 *
 * 每次迭代时测试的数据库数量不超过 CRON_DBS_PER_CALL = 16。
 *
 * 这种调用是在Redis检测到timelimit_exit为true时使用的.
 *
 * type：
 * ACTIVE_EXPIRE_CYCLE_FAST: 该函数将尝试运行一个“快速”过期周期，该周期不超过 EXPIRE_FAST_CYCLE_DURATION 微秒，并且在相同的时间之前不会再次重复。
 * ACTIVE_EXPIRE_CYCLE_SLOW: 执行正常的过期周期，其中时间限制是 ACTIVE_EXPIRE_CYCLE_SLOW_TIME_PERC 定义指定的 REDIS_HZ 周期的百分比
 * */

void activeExpireCycle(int type) {
    /* 这个函数有一些全局状态，为了能够在多次调用中持续工作 */
    static unsigned int current_db = 0; /* 上次测试的数据库。*/
    static int timelimit_exit = 0;      /* 上次调用达到时间限制？ */
    static long long last_fast_cycle = 0; /* 上次运行快速循环的时间。*/

    int j, iteration = 0;
    int dbs_per_call = CRON_DBS_PER_CALL; /*每次迭代检查的数据库数*/
    long long start = ustime(), timelimit, elapsed; /*开始时间，时间限制，经过的时间*/

    /*当客户端已暂停时，数据集应该是静态的，不仅从客户端无法写入的角度，还从过期和删除键的角度不能执行。*/
    if (clientsArePaused()) return;

    if (type == ACTIVE_EXPIRE_CYCLE_FAST) {
        /*如果上个循环没有达到时间限制，则不开始快速循环。
         * 也不要在与快速循环总持续时间相同的时间段内重复快速循环。*/
        if (!timelimit_exit) return;
        if (start < last_fast_cycle + ACTIVE_EXPIRE_CYCLE_FAST_DURATION * 2) return;
        last_fast_cycle = start;
    }

    /*我们通常应该在每次迭代中测试CRON_DBS_PER_CALL个数据库，有两个例外情况：
     *
     * 1) 服务器数据库数量小于CRON_DBS_PER_CALL。
     * 2) 如果上次达到了时间限制，我们希望在此迭代中扫描所有数据库，
     *    因为某些数据库中有工作要做，并且我们不希望过期的键占用太长时间的内存。*/
    if (dbs_per_call > server.dbnum || timelimit_exit)
        dbs_per_call = server.dbnum;

    /*我们可以每次迭代中使用最多ACTIVE_EXPIRE_CYCLE_SLOW_TIME_PERC 百分比的CPU时间。
     * 因为此函数以 server.hz 次每秒的频率调用，因此以下是我们可以在该函数中花费的最大微秒数。*/
    timelimit = 1000000 * ACTIVE_EXPIRE_CYCLE_SLOW_TIME_PERC / server.hz / 100;
    timelimit_exit = 0;
    if (timelimit <= 0) timelimit = 1;

    if (type == ACTIVE_EXPIRE_CYCLE_FAST)
        timelimit = ACTIVE_EXPIRE_CYCLE_FAST_DURATION; /*以微秒为单位。*/

    /*随着键的过期，我们累积一些全局统计信息，
     * 以了解在数据库中仍存在但逻辑上已过期的键的数量。*/
    long total_sampled = 0;
    long total_expired = 0;
    //OK,初始化完成,开始遍历
    for (j = 0; j < dbs_per_call && timelimit_exit == 0; j++) {
        int expired;
        //获取当前要处理的数据库
        redisDb *db = server.db + (current_db % server.dbnum);

        /*指向下一个要处理的数据库*/
        current_db++;

        /* 如果在循环结束时有超过25%的键已经过期，则继续过期。*/
        do {
            unsigned long num, slots;
            long long now, ttl_sum;
            int ttl_samples;
            iteration++;

            /* 如果当前数据库中没有键带过期时间,那么跳过这个数据库*/
            if ((num = dictSize(db->expires)) == 0) {
                db->avg_ttl = 0;
                break;
            }
            slots = dictSlots(db->expires);
            now = mstime();

            /* 当填充的槽少于1%时，获取随机键是昂贵的，所以在这里停止等待更好的时机...
             * 尽快调整字典大小。*/
            if (num && slots > DICT_HT_INITIAL_SIZE &&
                (num * 100 / slots < 1))
                break;

            /* 主收集循环。在具有到期时间的键中随机选择一些键并检查是否过期。*/
            expired = 0;
            ttl_sum = 0;
            ttl_samples = 0;

            if (num > ACTIVE_EXPIRE_CYCLE_LOOKUPS_PER_LOOP)
                num = ACTIVE_EXPIRE_CYCLE_LOOKUPS_PER_LOOP;

            while (num--) {
                dictEntry *de;
                long long ttl;

                if ((de = dictGetRandomKey(db->expires)) == NULL)
                    //随机获取一个带有过期时间的键
                    break;
                ttl = dictGetSignedIntegerVal(de) - now;
                if (activeExpireCycleTryExpire(db, de, now)) expired++;
                if (ttl > 0) {
                    /*我们要的是尚未过期的键的平均TTL。*/
                    ttl_sum += ttl;
                    ttl_samples++;
                }
                total_sampled++;
            }
            total_expired += expired;

            /* 更新此数据库的平均TTL统计信息。*/
            if (ttl_samples) {
                long long avg_ttl = ttl_sum / ttl_samples;

                /* 用一些样本做一个简单的加权平均。
                 * 我们只使用当前估计值的2%权重和上个估计值的98%权重。*/
                if (db->avg_ttl == 0) db->avg_ttl = avg_ttl;
                db->avg_ttl = (db->avg_ttl / 50) * 49 + (avg_ttl / 50);
            }

            /* 如果有太多键在当前数据库中找到超时，则我们不能永远阻塞在这里。
             * 因此，在给定的毫秒数后，返回调用者以等待其他活动过期循环。*/
            if ((iteration & 0xf) == 0) { /* 每16次检查一次。*/
                elapsed = ustime() - start;
                if (elapsed > timelimit) {
                    timelimit_exit = 1;
                    server.stat_expired_time_cap_reached_count++;
                    break;
                }
            }
            /* 如果当前数据库中找到的键小于25%，我们不会重复循环。*/
        } while (expired > ACTIVE_EXPIRE_CYCLE_LOOKUPS_PER_LOOP / 4);
    }

    elapsed = ustime() - start;
    latencyAddSampleIfNeeded("expire-cycle", elapsed / 1000);

    /* 更新我们对现有但尚未过期的键的估计。
     * 带有此样本的运行平均占5％。*/
    double current_perc;
    if (total_sampled) {
        current_perc = (double) total_expired / total_sampled;
    } else
        current_perc = 0;
    server.stat_expired_stale_perc = (current_perc * 0.05) +
                                     (server.stat_expired_stale_perc * 0.95);
}
/*-----------------------------------------------------------------------------
 * Expires of keys created in writable slaves
 *
 * Normally slaves do not process expires: they wait the masters to synthesize
 * DEL operations in order to retain consistency. However writable slaves are
 * an exception: if a key is created in the slave and an expire is assigned
 * to it, we need a way to expire such a key, since the master does not know
 * anything about such a key.
 *
 * In order to do so, we track keys created in the slave side with an expire
 * set, and call the expireSlaveKeys() function from time to time in order to
 * reclaim the keys if they already expired.
 *
 * Note that the use case we are trying to cover here, is a popular one where
 * slaves are put in writable mode in order to compute slow operations in
 * the slave side that are mostly useful to actually read data in a more
 * processed way. Think at sets intersections in a tmp key, with an expire so
 * that it is also used as a cache to avoid intersecting every time.
 *
 * This implementation is currently not perfect but a lot better than leaking
 * the keys as implemented in 3.2.
 *----------------------------------------------------------------------------*/

/* The dictionary where we remember key names and database ID of keys we may
 * want to expire from the slave. Since this function is not often used we
 * don't even care to initialize the database at startup. We'll do it once
 * the feature is used the first time, that is, when rememberSlaveKeyWithExpire()
 * is called.
 *
 * The dictionary has an SDS string representing the key as the hash table
 * key, while the value is a 64 bit unsigned integer with the bits corresponding
 * to the DB where the keys may exist set to 1. Currently the keys created
 * with a DB id > 63 are not expired, but a trivial fix is to set the bitmap
 * to the max 64 bit unsigned value when we know there is a key with a DB
 * ID greater than 63, and check all the configured DBs in such a case. */
dict *slaveKeysWithExpire = NULL;

/* Check the set of keys created by the master with an expire set in order to
 * check if they should be evicted. */
void expireSlaveKeys(void) {
    if (slaveKeysWithExpire == NULL ||
        dictSize(slaveKeysWithExpire) == 0)
        return;

    int cycles = 0, noexpire = 0;
    mstime_t start = mstime();
    while (1) {
        dictEntry *de = dictGetRandomKey(slaveKeysWithExpire);
        sds keyname = dictGetKey(de);
        uint64_t dbids = dictGetUnsignedIntegerVal(de);
        uint64_t new_dbids = 0;

        /* Check the key against every database corresponding to the
         * bits set in the value bitmap. */
        int dbid = 0;
        while (dbids && dbid < server.dbnum) {
            if ((dbids & 1) != 0) {
                redisDb *db = server.db + dbid;
                dictEntry *expire = dictFind(db->expires, keyname);
                int expired = 0;

                if (expire &&
                    activeExpireCycleTryExpire(server.db + dbid, expire, start)) {
                    expired = 1;
                }

                /* If the key was not expired in this DB, we need to set the
                 * corresponding bit in the new bitmap we set as value.
                 * At the end of the loop if the bitmap is zero, it means we
                 * no longer need to keep track of this key. */
                if (expire && !expired) {
                    noexpire++;
                    new_dbids |= (uint64_t) 1 << dbid;
                }
            }
            dbid++;
            dbids >>= 1;
        }

        /* Set the new bitmap as value of the key, in the dictionary
         * of keys with an expire set directly in the writable slave. Otherwise
         * if the bitmap is zero, we no longer need to keep track of it. */
        if (new_dbids)
            dictSetUnsignedIntegerVal(de, new_dbids);
        else
            dictDelete(slaveKeysWithExpire, keyname);

        /* Stop conditions: found 3 keys we cna't expire in a row or
         * time limit was reached. */
        cycles++;
        if (noexpire > 3) break;
        if ((cycles % 64) == 0 && mstime() - start > 1) break;
        if (dictSize(slaveKeysWithExpire) == 0) break;
    }
}

/* Track keys that received an EXPIRE or similar command in the context
 * of a writable slave. */
void rememberSlaveKeyWithExpire(redisDb *db, robj *key) {
    if (slaveKeysWithExpire == NULL) {
        static dictType dt = {
                dictSdsHash,                /* hash function */
                NULL,                       /* key dup */
                NULL,                       /* val dup */
                dictSdsKeyCompare,          /* key compare */
                dictSdsDestructor,          /* key destructor */
                NULL                        /* val destructor */
        };
        slaveKeysWithExpire = dictCreate(&dt, NULL);
    }
    if (db->id > 63) return;

    dictEntry *de = dictAddOrFind(slaveKeysWithExpire, key->ptr);
    /* If the entry was just created, set it to a copy of the SDS string
     * representing the key: we don't want to need to take those keys
     * in sync with the main DB. The keys will be removed by expireSlaveKeys()
     * as it scans to find keys to remove. */
    if (de->key == key->ptr) {
        de->key = sdsdup(key->ptr);
        dictSetUnsignedIntegerVal(de, 0);
    }

    uint64_t dbids = dictGetUnsignedIntegerVal(de);
    dbids |= (uint64_t) 1 << db->id;
    dictSetUnsignedIntegerVal(de, dbids);
}

/* Return the number of keys we are tracking. */
size_t getSlaveKeyWithExpireCount(void) {
    if (slaveKeysWithExpire == NULL) return 0;
    return dictSize(slaveKeysWithExpire);
}

/* Remove the keys in the hash table. We need to do that when data is
 * flushed from the server. We may receive new keys from the master with
 * the same name/db and it is no longer a good idea to expire them.
 *
 * Note: technically we should handle the case of a single DB being flushed
 * but it is not worth it since anyway race conditions using the same set
 * of key names in a wriatable slave and in its master will lead to
 * inconsistencies. This is just a best-effort thing we do. */
void flushSlaveKeysWithExpireList(void) {
    if (slaveKeysWithExpire) {
        dictRelease(slaveKeysWithExpire);
        slaveKeysWithExpire = NULL;
    }
}

int checkAlreadyExpired(long long when) {
    /* EXPIRE with negative TTL, or EXPIREAT with a timestamp into the past
     * should never be executed as a DEL when load the AOF or in the context
     * of a slave instance.
     *
     * Instead we add the already expired key to the database with expire time
     * (possibly in the past) and wait for an explicit DEL from the master. */
    return (when <= mstime() && !server.loading && !server.masterhost);
}

/*-----------------------------------------------------------------------------
 * Expires Commands
 *----------------------------------------------------------------------------*/

/*
 * expireat/pexpire/setex/psetex,
 * 或者带EX,PX选项的set命令,
 * 都是这个函数处理的
 * */
void expireGenericCommand(client *c, long long basetime, int unit) {
    robj *key = c->argv[1], *param = c->argv[2];
    long long when; /* unix time in milliseconds when the key will expire. */

    if (getLongLongFromObjectOrReply(c, param, &when, NULL) != C_OK)
        return;

    if (unit == UNIT_SECONDS) when *= 1000;
    when += basetime;

    /* No key, return zero. */
    if (lookupKeyWrite(c->db, key) == NULL) {
        addReply(c, shared.czero);
        return;
    }

    if (checkAlreadyExpired(when)) {
        robj *aux;

        int deleted = server.lazyfree_lazy_expire ? dbAsyncDelete(c->db, key) :
                      dbSyncDelete(c->db, key);
        serverAssertWithInfo(c, key, deleted);
        server.dirty++;

        /* Replicate/AOF this as an explicit DEL or UNLINK. */
        aux = server.lazyfree_lazy_expire ? shared.unlink : shared.del;
        rewriteClientCommandVector(c, 2, aux, key);
        signalModifiedKey(c->db, key);
        notifyKeyspaceEvent(NOTIFY_GENERIC, "del", key, c->db->id);
        addReply(c, shared.cone);
        return;
    } else {
        setExpire(c, c->db, key, when);
        addReply(c, shared.cone);
        signalModifiedKey(c->db, key);
        notifyKeyspaceEvent(NOTIFY_GENERIC, "expire", key, c->db->id);
        server.dirty++;
        return;
    }
}

/* EXPIRE key seconds */
void expireCommand(client *c) {
    expireGenericCommand(c, mstime(), UNIT_SECONDS);
}

/* EXPIREAT key time */
void expireatCommand(client *c) {
    expireGenericCommand(c, 0, UNIT_SECONDS);
}

/* PEXPIRE key milliseconds */
void pexpireCommand(client *c) {
    expireGenericCommand(c, mstime(), UNIT_MILLISECONDS);
}

/* PEXPIREAT key ms_time */
void pexpireatCommand(client *c) {
    expireGenericCommand(c, 0, UNIT_MILLISECONDS);
}

/* Implements TTL and PTTL */
void ttlGenericCommand(client *c, int output_ms) {
    long long expire, ttl = -1;

    /* If the key does not exist at all, return -2 */
    if (lookupKeyReadWithFlags(c->db, c->argv[1], LOOKUP_NOTOUCH) == NULL) {
        addReplyLongLong(c, -2);
        return;
    }
    /* The key exists. Return -1 if it has no expire, or the actual
     * TTL value otherwise. */
    expire = getExpire(c->db, c->argv[1]);
    if (expire != -1) {
        ttl = expire - mstime();
        if (ttl < 0) ttl = 0;
    }
    if (ttl == -1) {
        addReplyLongLong(c, -1);
    } else {
        addReplyLongLong(c, output_ms ? ttl : ((ttl + 500) / 1000));
    }
}

/* TTL key */
void ttlCommand(client *c) {
    ttlGenericCommand(c, 0);
}

/* PTTL key */
void pttlCommand(client *c) {
    ttlGenericCommand(c, 1);
}

/* PERSIST key */
void persistCommand(client *c) {
    if (lookupKeyWrite(c->db, c->argv[1])) {
        if (removeExpire(c->db, c->argv[1])) {
            addReply(c, shared.cone);
            server.dirty++;
        } else {
            addReply(c, shared.czero);
        }
    } else {
        addReply(c, shared.czero);
    }
}

/* TOUCH key1 [key2 key3 ... keyN] */
void touchCommand(client *c) {
    int touched = 0;
    for (int j = 1; j < c->argc; j++)
        if (lookupKeyRead(c->db, c->argv[j]) != NULL) touched++;
    addReplyLongLong(c, touched);
}

