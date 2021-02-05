# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 20:14
# @Author  : tmb
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


'''
思路：双指针，新建4个结点
'''


class Solution:
    def partition(self, head: ListNode, x: int) -> ListNode:
        before, after = ListNode(0), ListNode(0)
        before_head, after_head = before, after
        while head:
            if head.val < x:
                before.next = head
                before = before.next
            elif head.val >= x:
                after.next = head
                after = after.next
            head = head.next
        after.next = None #添加这个
        before.next = after_head.next
        return before_head.next
