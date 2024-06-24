# -*- coding: utf-8 -*-
# @Time    : 2020/12/17 20:16
# @Author  : tmb
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    def deleteDuplicates(self, head):
        if not (head and head.next):
            return head
        pre = ListNode(-1)
        pre.next = head
        slow, fast = pre, head
        while fast and fast.next:
            # 初始化的时a指向的是哑结点，所以比较逻辑应该是a的下一个节点和b的下一个节点
            if slow.next.val != fast.next.val:
                slow = slow.next
                fast = fast.next
            else:
                # 如果a、b指向的节点值相等，就不断移动b，直到a、b指向的值不相等 
                while fast and fast.next and slow.next.val == fast.next.val:
                    fast = fast.next
                slow.next = fast.next
                fast = fast.next
        return pre.next
