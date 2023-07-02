/* Allocator selection.
 *
 * This file is used in order to change the Rax allocator at compile time.
 * Just define the following defines to what you want to use. Also add
 * the include of your alternate allocator if needed (not needed in order
 * to use the default libc allocator). */

#ifndef LISTPACK_ALLOC_H
#define LISTPACK_ALLOC_H

#include "zmalloc.h"

#define lp_malloc zmalloc
#define lp_realloc zrealloc
#define lp_free zfree
#endif
