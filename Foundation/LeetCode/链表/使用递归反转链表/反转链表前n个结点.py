# -*- coding: utf-8 -*-
# @Time    : 2020/12/10 14:42
# @Author  : tmb

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def reverseList(self, head: ListNode, n) -> ListNode:
        if not head:
            return None
        if not n:
            return head
        next_normal = None
        if n == 1:
            next_normal = head.next
            return head
        last = self.reverseList(head.next, n - 1)
        head.next.next = head
        head.next = next_normal
        return last
