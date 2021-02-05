# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 15:47
# @Author  : tmb
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def removeElements(self, head: ListNode, val: int) -> ListNode:
        hair = ListNode(0)
        hair.next = head
        pre, cur = hair, head
        while cur:
            if cur.val == val:
                pre.next = cur.next
                cur = cur.next
            else:
                pre = cur
                cur = cur.next
        return hair.next
