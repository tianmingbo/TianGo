# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 9:23
# @Author  : tmb
# class ListNode:
def __init__(self, x):
    self.val = x
    self.next = None


'''
解法一：集合，记录index
解法二：数学推导。slow，fast指针，如果有环，会在环内相遇。此时，fast等于head，每次跳一个结点，下次相遇会指向入口

'''


class Solution1:
    def detectCycle(self, head):
        if head is None or head.next is None:
            return None
        a = set()
        p = head
        while p:
            if p not in a:
                a.add(p)
                p = p.next
            else:
                return p
        return None


class Solution2:
    def detectCycle(self, head):
        try:
            fast = head.next
            slow = head
            while fast != slow:
                fast = fast.next.next
                slow = slow.next
        except:
            return None
        slow = slow.next
        while head != slow:
            head = head.next
            slow = slow.next
        return head
