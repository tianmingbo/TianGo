# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 9:53
# @Author  : tmb
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def isSubStructure(self, A: TreeNode, B: TreeNode) -> bool:
        if not A or not B:
            return False

        def helper(A, B):
            if not B:
                return True
            if not A or A.val != B.val:
                return False
            return helper(A.left, B.left) and helper(A.right, B.right)

        return helper(A, B) or self.isSubStructure(A.left, B) or self.isSubStructure(A.right, B)