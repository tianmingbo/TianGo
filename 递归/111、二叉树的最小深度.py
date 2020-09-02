# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 14:12
# @Author  : tmb
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def minDepth(self, root) -> int:
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        left = self.minDepth(root.left)
        right = self.minDepth(root.right)
        return min(left, right) + 1
