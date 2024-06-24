# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 18:57
# @Author  : tmb
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head:
            return head
        if head.next is None:
            return head
        last = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return last
