# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 20:58
# @Author  : tmb
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


'''
互相走，node1走node2的路，
node2走node1的路，最终两个走的距离一样。
不相交的话，最后都为空
'''


class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        node1, node2 = headA, headB
        while node1 != node2:
            if node1:
                node1 = node1.next
            else:
                node1 = headB
            if node2:
                node2 = node2.next
            else:
                node2 = headA
        return node1
