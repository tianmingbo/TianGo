#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define AL_START_HEAD 0
#define AL_START_TAIL 1
#define listLength(l) ((l)->len)
typedef struct listNode
{
    struct listNode *prev; //指向前置节点
    struct listNode *next; //下一个节点
    void *value;
} listNode;

typedef struct listIter
{
    listNode *next;
    int direction;
} listIter;

//双端列表，直接取到最后一个
typedef struct list
{
    listNode *head;
    listNode *tail;
    void *(*dup)(void *ptr);
    void (*free)(void *ptr);
    void (*match)(void *ptr, void *key);
    unsigned long len;
} list;

list *listCreate(void)
{
    struct list *list;
    if ((list = malloc(sizeof(*list))) == NULL)
        return NULL;
    list->head = list->tail = NULL;
    list->len = 0;
    list->dup = NULL;
    list->free = NULL;
    list->match = NULL;
    return list;
}

void listRelease(list *list)
{
    unsigned long len;
    listNode *current, *next;
    len = list->len;
    current = list->head;
    while (len--)
    {
        next = current->next;
        if (list->free)
            list->free(current->value);
        free(current);
        current = next;
    }
    free(list);
}

list *listAddNodeHead(list *list, void *value)
{
    listNode *node;
    if ((node = malloc(sizeof(*node))) == NULL)
        return NULL;
    node->value = value;
    if (list->len == 0)
    {
        list->head = list->tail = node;
        node->prev = node->next = NULL;
    }
    else
    {
        node->prev = NULL;
        node->next = list->head;
        list->head->prev = node;
        list->head = node;
    }
    list->len++;
    return list;
}

list *listAddNodeTail(list *list, void *value)
{
    listNode *node;
    if ((node = malloc(sizeof(*node))) == NULL)
        return NULL;
    node->value = value;
    if (list->len == 0)
    {
        list->head = list->tail = node;
        node->prev = node->next = NULL;
    }
    else
    {
        node->prev = list->tail;
        node->next = NULL;
        list->tail->next = node;
        list->tail = node;
    }
    list->len++;
    return list;
}

list *listInsertNode(list *list, listNode *old_node, void *value, int after)
{
    listNode *node;
    if ((node = malloc(sizeof(*node))) == NULL)
        return NULL;
    node->value = value;
    if (after)
    {
        node->prev = old_node;
        node->next = old_node->next;
        if (list->tail == old_node)
        {
            list->tail = node;
        }
    }
    else
    {
        node->next = old_node;
        node->prev = old_node->prev;
        if (list->head == old_node)
            list->head = old_node;
    }
    if (node->prev != NULL)
    {
        node->prev->next = node;
    }
    if (node->next != NULL)
    {
        node->next->prev = node;
    }
    list->len++;
    return list;
}

void listDelNode(list *list, listNode *node)
{
    if (node->prev)
        node->prev->next = node->next; //删除的node不是头节点
    else
        list->head = node->next;
    if (node->next)
        node->next->prev = node->prev;
    else
        list->tail = node->prev;

    if (list->free)
        list->free(node->value);

    free(node);
    list->len--;
}

listIter *listGetIterator(list *list, int direction)
{
    listIter *iter;
    if ((iter = malloc(sizeof(*iter))) == NULL)
        return NULL;
    if (direction == AL_START_HEAD)
        iter->next = list->head;
    else
        iter->next = list->tail;
    iter->direction = direction;
    return iter;
}

void listReleaseIterator(listIter *iter)
{
    free(iter);
}

void listRewind(list *list, listIter *li)
{
    li->next = list->head;
    li->direction = AL_START_HEAD;
}

void listRewIndTail(list *list, listIter *li)
{
    li->next = list->tail;
    li->direction = AL_START_TAIL;
}

listNode *listNext(listIter *iter)
{
    listNode *current = iter->next;
    if (current != NULL)
    {
        if (iter->direction == AL_START_HEAD)
            iter->next = current->next;
        else
            iter->next = current->prev;
    }
    return current;
}

//复制一个给定链表的副本
list *listDup(list *orig)
{
    list *copy;
    listIter *iter;
    listNode *node;
    if ((copy = listCreate()) == NULL)
        return NULL;
    copy->dup = orig->dup;
    copy->free = orig->free;
    copy->match = orig->match;
    iter = listGetIterator(orig, AL_START_HEAD);
    while ((node = listNext(iter)) != NULL)
    {
        void *value;
        if (copy->dup)
        {
            value = copy->dup(node->value);
            if (value == NULL)
            {
                listRelease(copy);
                listReleaseIterator(iter);
                return NULL;
            }
        }
        else
            value = node->value;
        if (listAddNodeTail(copy, value) == NULL)
        {
            listRelease(copy);
            listReleaseIterator(iter);
            return NULL;
        }
    }
    listReleaseIterator(iter);
    return copy;
}

listNode *listSearchKey(list *list, void *key)
{
    listIter *iter;
    listNode *node;
    iter = listGetIterator(list, AL_START_HEAD);
    while ((node = listNext(iter)) != NULL)
    {
        if (list->match)
        {
            if (list->match(node->value, key))
            {
                listReleaseIterator(iter);
                return node;
            }
        }
        else
        {
            if (key == node->value)
            {
                listReleaseIterator(iter);
                return node;
            }
        }
    }
    listReleaseIterator(iter);
    return NULL;
}

listNode *listIndex(list *list, long index)
{
    listNode *n;
    if (index < 0)
    {
        index = (-index) - 1;
        while (index-- && n)
            n = n->prev;
    }
    else
    {
        n = list->head;
        while (index-- && n)
            n = n->next;
    }
    return n;
}

void listRotate(list *list)
{
    listNode *tail = list->tail; //取出尾节点
    if (listLength(list) <= 1)
        return;
    list->tail = tail->prev;
    list->tail->next = NULL;
    //插入到表头
    list->head->prev = tail;
    tail->prev = NULL;
    tail->next = list->head;
    list->head = tail;
}

int main(int argc, char const *argv[])
{
    struct list *list;
    printf("%p\n", list);
    printf("%lu", sizeof(list->head));
    return 0;
}
