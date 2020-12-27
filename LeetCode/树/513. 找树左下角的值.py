# -*- coding: utf-8 -*-
# @Time    : 2020/12/26 18:17
# @Author  : tmb
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def findBottomLeftValue(self, root: TreeNode) -> int:
        queue = [root]
        res = []
        while queue:
            tmp = []
            for i in range(len(queue)):
                node = queue.pop(0)
                tmp.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            res.append(tmp)
        return res[-1][0]