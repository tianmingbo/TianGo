# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 19:37
# @Author  : tmb
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        if not p and not q:  # 如果都不存在
            return True
        if not p or not q or p.val != q.val:  # 如果两棵树的左右节点不一致，或者值不相等
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
