# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 15:22
# @Author  : tmb
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# 中序遍历是升序
class Solution:
    def getMinimumDifference(self, root: TreeNode) -> int:
        self.res = []
        self.get_all_node(root)
        if len(self.res) < 2:
            return self.res[0]
        min_res = float('inf')
        for i in range(1, len(self.res)):
            min_res = min(min_res, self.res[i] - self.res[i - 1])
        return min_res

    def get_all_node(self, root):
        if not root:
            return
        self.get_all_node(root.left)
        self.res.append(root.val)
        self.get_all_node(root.right)
