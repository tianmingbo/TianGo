# -*- coding: utf-8 -*-
# @Time    : 2020/12/14 20:00
# @Author  : tmb
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        cur = head
        for _ in range(k):
            if not cur:
                return head
            cur = cur.next

        pre, cur = None, head
        for _ in range(k):
            cur.next, pre, cur = pre, cur, cur.next

        head.next = self.reverseKGroup(cur, k)
        return pre

    def reverseKGroup2(self, head, k):
        dummy = jump = ListNode(0)
        dummy.next = l = r = head

        while True:
            count = 0
            while r and count < k:  # use r to locate the range
                r = r.next
                count += 1
            if count == k:  # if size k satisfied, reverse the inner linked list
                pre, cur = r, l
                for _ in range(k):
                    cur.next, cur, pre = pre, cur.next, cur  # standard reversing
                jump.next, jump, l = pre, l, r  # connect two k-groups
            else:
                return dummy.next
