# -*- coding: utf-8 -*-
# @Time    : 2020/11/14 16:54
# @Author  : tmb
class Solution:
    def swapPairs(self, head):
        if not head or not head.next:
            return head
        first = head
        second = head.next
        second.next, first.next = first, self.swapPairs(second.next)  # 递归
        return second


'''

'''


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution2:
    def swapPairs(self, head: ListNode) -> ListNode:
        tailhead = ListNode(0)  # 新建一个头结点
        tailhead.next = head
        tmp = tailhead
        while tmp.next and tmp.next.next:
            node1 = tmp.next
            node2 = tmp.next.next
            tmp.next = node2
            node1.next = node2.next
            node2.next = node1
            tmp = node1
        return tailhead.next
