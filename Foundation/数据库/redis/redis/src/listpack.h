/* Listpack -- A lists of strings serialization format
 */

#ifndef __LISTPACK_H
#define __LISTPACK_H

#include <stdint.h>

#define LP_INTBUF_SIZE 21 /* 20 digits of -2^63 + 1 null term = 21. */

/* lpInsert() where argument possible values: */
#define LP_BEFORE 0
#define LP_AFTER 1
#define LP_REPLACE 2

unsigned char *lpNew(void);

void lpFree(unsigned char *lp);

unsigned char *
lpInsert(unsigned char *lp, unsigned char *ele, uint32_t size, unsigned char *p, int where, unsigned char **newp);

unsigned char *lpAppend(unsigned char *lp, unsigned char *ele, uint32_t size);

unsigned char *lpDelete(unsigned char *lp, unsigned char *p, unsigned char **newp);

uint32_t lpLength(unsigned char *lp);

unsigned char *lpGet(unsigned char *p, int64_t *count, unsigned char *intbuf);

unsigned char *lpFirst(unsigned char *lp);

unsigned char *lpLast(unsigned char *lp);

unsigned char *lpNext(unsigned char *lp, unsigned char *p);

unsigned char *lpPrev(unsigned char *lp, unsigned char *p);

uint32_t lpBytes(unsigned char *lp);

unsigned char *lpSeek(unsigned char *lp, long index);

#endif
