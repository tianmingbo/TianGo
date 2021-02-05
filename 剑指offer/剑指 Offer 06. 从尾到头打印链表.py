# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 20:36
# @Author  : tmb
# Definition for singly-linked list.
from typing import List


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def reversePrint(self, head: ListNode) -> List[int]:
        if not head:
            return []
        res = []
        while head:
            res.append(head.val)
            head = head.next
        return res[::-1]
