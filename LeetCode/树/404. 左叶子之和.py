# -*- coding: utf-8 -*-
# @Time    : 2020/12/26 17:59
# @Author  : tmb
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def sumOfLeftLeaves(self, root: TreeNode) -> int:
        if not root:
            return 0
        left_val = 0
        if root.left and not root.left.left and not root.left.right:  # 判断左结点存在
            left_val = root.left.val
        return left_val + self.sumOfLeftLeaves(root.left) + self.sumOfLeftLeaves(root.right)


class Solution2:
    res = 0
    def sumOfLeftLeaves(self, root: TreeNode) -> int:
        if not root:
            return 0
        if root.left and not root.left.left and not root.left.right:  # 判断左结点存在
            self.res += root.left.val
        self.sumOfLeftLeaves(root.left)
        self.sumOfLeftLeaves(root.right)
        return self.res
