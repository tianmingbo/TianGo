# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 20:28
# @Author  : tmb
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def rotateRight(self, head: ListNode, k: int) -> ListNode:
        len_listnode = 0
        p, tail = head, head
        end = ListNode(0)
        while tail.next:  # 找到长度，获得尾结点
            len_listnode += 1
            tail = tail.next
            end = tail
        k = k % len_listnode  # 翻转长度
        for i in range(len_listnode - k):  # 翻转的前一个结点
            p = p.next
            k -= 1
        cur = p.next  # 翻转后的头结点
        p.next = None
        end.next = head
        return cur
