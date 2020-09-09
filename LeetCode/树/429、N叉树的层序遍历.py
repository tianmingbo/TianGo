# -*- coding: utf-8 -*-
# @Time    : 2020/8/26 21:53
# @Author  : tmb

"""
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
"""


# 使用队列  层序遍历
class Solution:
    def levelOrder(self, root):
        if not root:
            return []
        queue = [root]
        res = []
        while queue:
            res.append([node.val for node in queue])  # 遍历每层每个节点的值
            queue = [child for node in queue for child in node.children]  # 记录当前层的所有子节点
        return res
