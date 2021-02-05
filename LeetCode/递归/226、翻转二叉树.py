# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 10:21
# @Author  : tmb
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    def invertTree(self, root):
        # if not root:
        #     return
        # left = self.invertTree(root.left)
        # right = self.invertTree(root.right)
        # root.left = right
        # root.right = left
        # return root
        if not root:
            return
        left = self.invertTree(root.left)
        right = self.invertTree(root.right)
        root.left, root.right = right, left
        return root
