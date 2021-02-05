# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 20:46
# @Author  : tmb
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def sortList(self, head: ListNode) -> ListNode:
        if not head:
            return head
        tmp = []
        while head:
            tmp.append(head)
            head = head.next
        return sorted(head, key=head.val)
