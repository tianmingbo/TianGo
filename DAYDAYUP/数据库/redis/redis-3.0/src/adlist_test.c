#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct listNode
{
    struct listNode *prev; //指向前置节点
    struct listNode *next; //下一个节点
    void *value;
} listNode;

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

list *ListCreate(void)
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

list *listAddTail(list *list, void *value)
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

int main(int argc, char const *argv[])
{
    struct list *list;
    printf("%p\n", list);
    printf("%lu", sizeof(list->head));
    return 0;
}
