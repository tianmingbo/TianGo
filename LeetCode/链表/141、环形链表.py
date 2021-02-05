# -*- coding: utf-8 -*-
# @Time    : 2020/11/15 10:42
# @Author  : tmb
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


'''
快慢指针，快两倍，终会相遇
'''


class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
            if slow == fast:
                return True
        return False
