# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 20:30
# @Author  : tmb
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def rightSideView(self, root: TreeNode) -> List[int]:
        if not root:
            return []
        queue = [root.val]
        res = []
        while queue:
            tmp = []
            for i in range(len(queue)):
                if len(queue) == 1:
                    res.append(queue[0].val)
                node = queue.pop(0)
                if node.left:
                    tmp.append(node.left)
                if node.right:
                    tmp.append(node.right)
            queue = tmp[:]
        return res
