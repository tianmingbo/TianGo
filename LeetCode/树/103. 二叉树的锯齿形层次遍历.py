# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 20:20
# @Author  : tmb
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


from typing import List


class Solution:
    def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        queue = [root, ]
        res, layer = [], 0
        while queue:
            tmp = []
            for i in range(len(queue)):
                cur = queue.pop(0)
                tmp.append(cur.val)
                if cur.left:
                    queue.append(cur.left)
                if cur.right:
                    queue.append(cur.right)
            if layer % 2 == 0:
                res.append(tmp)
            else:
                res.append(tmp[::-1])
            layer += 1
        return res
