# -*- coding: utf-8 -*-
# @Time    : 2020/11/14 16:15
# @Author  : tmb

class Solution:
    def reverseList(self, head):
        p = head
        q = None
        while p:
            q, q.next, p = p, q, p.next  # 直接反转
        return q
