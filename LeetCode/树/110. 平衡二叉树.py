# -*- coding: utf-8 -*-
# @Time    : 2020/12/17 19:35
# @Author  : tmb
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        if not root:
            return True
        if abs(self.max_depth(root.left) - self.max_depth(root.right)) >= 2:  # 每次递归调用，获取高度
            return False

        return self.isBalanced(root.left) and self.isBalanced(root.right)

    def max_depth(self, root):
        if not root:
            return 0
        left = self.max_depth(root.left)
        right = self.max_depth(root.right)
        return max(left, right) + 1
