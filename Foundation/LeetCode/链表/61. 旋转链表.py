# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 20:28
# @Author  : tmb
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def rotateRight(self, head: ListNode, k: int) -> ListNode:
        if not head or not head.next:
            return head
        p = head
        len_node = 1
        while p.next:  # 获取链表长度
            p = p.next
            len_node += 1
        p.next = head  # 尾指向头
        new_pre = head
        for i in range(len_node - (k % len_node + 1)):  # 翻转前的那个结点
            new_pre = new_pre.next
        new_head = new_pre.next  # 翻转结点
        new_pre.next = None
        return new_head
