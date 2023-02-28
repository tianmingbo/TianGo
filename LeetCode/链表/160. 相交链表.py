from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        # 两个；链表拼接在一起，有交点会走到交叉
        q, p = headA, headB
        while p != q:
            p = p.next if p else headB
            q = q.next if q else headA
        return p
