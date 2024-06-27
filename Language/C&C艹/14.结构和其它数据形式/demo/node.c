#include "stdio.h"

struct NODE {
    int a;
    struct NODE *b;
    struct NODE *c;
};
struct NODE nodes[5] = {
        {5,  nodes + 3, NULL},//200~212
        {15, nodes + 4, nodes + 3},//212~224
        {22, NULL,      nodes + 4},//224~236
        {12, nodes + 1, nodes},//236~248
        {18, nodes + 2, nodes + 1}//248~260
};
struct NODE *np = nodes + 2;
struct NODE **npp = &nodes[1].b;

/**
 * 对下面每个表达式求值,并写出它的值。同时,写明任何表过达式求值过程中可能出现的副作用。
 * 你应该用最初显示的值对每个表达式求值(也就就是说,不要使用某个表达式的结果来对下一个表达式求值)。
 * 假定 nodes数组在内存中的起始位置为200,并且在这台机器上整数和指针的长度都是4个字节。
nodes是nodes数组的第一个元素,即 {5,  nodes + 3, NULL}

nodes               200
nodes.a             非法
nodes[3].a          12
nodes[3].c          200
nodes[3].c->a       5
*nodes              {5,nodes+3,NULL}
*nodes.a            非法
(*nodes).a          5
nodes->a            5
nodes[3].b->b       248
*nodes[3].b->b      {18, nodes + 2, nodes + 1}
&nodes              200
&nodes[3].a         236
&nodes[3].c         244
&nodes[3].c->a      200
&nodes->a           200
np                  224
np->a               22
np->c->c->a         15
npp                 216
npp->a              非法 npp指向的是 nodes[1].b 的地址
*npp                248
**npp               {18, nodes + 2, nodes + 1}
*npp->a             非法
(*npp)->a            18
&np                 未知
&np->a              224
&np->c->c->a        212
*/

