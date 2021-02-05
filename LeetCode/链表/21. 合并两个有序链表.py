# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 11:25
# @Author  : tmb
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        head = ListNode()
        p = head
        tmp1, tmp2 = l1, l2
        while tmp1 and tmp2:
            if tmp1.val <= tmp2.val:
                p.next = tmp1
                tmp1 = tmp1.next
            else:
                p.next = tmp2
                tmp2 = tmp2.next
            p = p.next
        while tmp1:  # 链表没用完,追加
            p.next = tmp1
            break
        while tmp2:
            p.next = tmp2
            break
        return head.next
