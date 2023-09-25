
#ifndef __INTSET_H
#define __INTSET_H

#include <stdint.h>

typedef struct intset {
    uint32_t encoding; //编码格式,int16_t,int32_t,int64_t
    uint32_t length; //元素数量
    int8_t contents[]; //存储元素数据,元素必须排序,并且无重复
} intset;

intset *intsetNew(void);

intset *intsetAdd(intset *is, int64_t value, uint8_t *success);

intset *intsetRemove(intset *is, int64_t value, int *success);

uint8_t intsetFind(intset *is, int64_t value);

int64_t intsetRandom(intset *is);

uint8_t intsetGet(intset *is, uint32_t pos, int64_t *value);

uint32_t intsetLen(const intset *is);

size_t intsetBlobLen(intset *is);

#ifdef REDIS_TEST
int intsetTest(int argc, char *argv[]);
#endif

#endif // __INTSET_H
