# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 18:19
# @Author  : tmb
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def deleteNode(self, head: ListNode, val: int) -> ListNode:
        if not head:
            return head
        pre = ListNode(0)
        pre.next = head
        p = pre
        while head:
            if head.val == val:
                p.next = head.next
                head = p.next
            else:
                head = head.next
                p = p.next
        return pre.next
