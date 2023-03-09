# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 18:49
# @Author  : tmb
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def getKthFromEnd(self, head: ListNode, k: int) -> ListNode:
        if not head:
            return head
        path = []
        while head:
            path.append(head)
            head = head.next
        return path[-k]


class Solution2:
    def getKthFromEnd(self, head: ListNode, k: int) -> ListNode:
        former, latter = head, head
        for _ in range(k):
            if not former:
                return
            former = former.next
        while former:
            former, latter = former.next, latter.next
        return latter
