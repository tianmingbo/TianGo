/*
* all.c -- Lua core, libraries and interpreter in a single file
*/

#define luaall_c

#include "../src/lapi.c"
#include "../src/lcode.c"
#include "../src/ldebug.c"
#include "../src/ldo.c"
#include "../src/ldump.c"
#include "../src/lfunc.c"
#include "../src/lgc.c"
#include "../src/llex.c"
#include "../src/lmem.c"
#include "../src/lobject.c"
#include "../src/lopcodes.c"
#include "../src/lparser.c"
#include "../src/lstate.c"
#include "../src/lstring.c"
#include "../src/ltable.c"
#include "../src/ltm.c"
#include "../src/lundump.c"
#include "../src/lvm.c"
#include "../src/lzio.c"

#include "../src/lauxlib.c"
#include "../src/lbaselib.c"
#include "../src/ldblib.c"
#include "../src/liolib.c"
#include "../src/linit.c"
#include "../src/lmathlib.c"
#include "../src/loadlib.c"
#include "../src/loslib.c"
#include "../src/lstrlib.c"
#include "../src/ltablib.c"

#include "../src/lua.c"
