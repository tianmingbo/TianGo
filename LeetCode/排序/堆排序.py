# -*- coding: utf-8 -*-
# @Time    : 2020/10/19 10:54
# @Author  : tmb
import random


def maxHeapfy(alist, length, parent):
    left = 2 * parent + 1
    right = 2 * parent + 2
    largest = parent

    # 找出根和左右孩子的最大值
    if left < length and alist[left] > alist[largest]:
        largest = left
    if right < length and alist[right] > alist[largest]:
        largest = right
    if largest != parent:  # 如果根不是最大值，就交换最大值，然后再递归调整
        alist[largest], alist[parent] = alist[parent], alist[largest]
        maxHeapfy(alist, length, largest)  # 递归构建
    print(alist)


def buildMaxHeap(alist):  # 构建最大堆
    n = len(alist)
    lastParent = (n - 1) // 2
    for i in range(lastParent, -1, -1):
        maxHeapfy(alist, n, i)


def heapSort(alist):
    buildMaxHeap(alist)
    n = len(alist)
    for i in range(n - 1, -1, -1):
        alist[0], alist[i] = alist[i], alist[0]  # 将最大值放在最后面
        maxHeapfy(alist, i, 0)
    return alist


'''
思想：根节点最大，大顶堆，对应升序，根节点最小，小顶堆。

构建大根堆，完全二叉树结构，初始无序
最大堆调整，进行堆排序。将堆顶元素与最后一个元素交换，此时后面有序
时间复杂度$O(nlogn)$，原地排序，不稳定  
建堆复杂度为O(n)，维护堆为O(logn)
'''
if __name__ == '__main__':
    a = [2, 7, 4, 1, 8, 1]
    print(heapSort(a))
    # alist = [2, 4, 1, 2, 5, 58, 45, 24, 24]
    # print(heapSort(alist))
    # b = [random.randint(1, 1000) for i in range(1000)]
    # print(b)
    # print(heapSort(b))
