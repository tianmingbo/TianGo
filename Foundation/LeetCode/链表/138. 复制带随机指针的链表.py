# -*- coding: utf-8 -*-
# @Time    : 2021/1/20 20:32
# @Author  : tmb

class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution(object):
    def copyRandomList(self, head):
        if not head:
            return head
        dic = {}
        p = head
        while p:
            # key是原节点，value是新节点
            dic[p] = Node(p.val, None, None)
            p = p.next
        p = head
        while p:
            # 遍历原节点，构造
            if p.random:
                dic[p].random = dic[p.random]
            if p.next:
                dic[p].next = dic[p.next]
            p = p.next
        return dic[head]
