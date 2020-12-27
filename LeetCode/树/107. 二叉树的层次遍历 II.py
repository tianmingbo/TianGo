# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 20:10
# @Author  : tmb
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def levelOrderBottom(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        res = []
        queue = [root, ]
        while queue:
            tmp = []
            for i in range(len(queue)):
                cur = queue.pop(0)
                tmp.append(cur.val)
                if cur.left:
                    queue.append(cur.left)
                if cur.right:
                    queue.append(cur.right)
            res.append(tmp)
        return res[::-1]
