# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 19:13
# @Author  : tmb
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    res = []

    def kthLargest(self, root: TreeNode, k: int) -> int:
        self.inorder(root)
        return self.res[-k]

    def inorder(self, root):
        if not root:
            return
        self.inorder(root.left)
        self.res.append(root.val)
        self.inorder(root.right)

    def kthLargest2(self, root: TreeNode, k: int) -> int:
        def dfs(root):
            if not root:
                return
            dfs(root.right)
            if self.k == 0:
                return
            self.k -= 1
            if self.k == 0:
                self.ans = root.val
            dfs(root.left)

        self.k = k
        dfs(root)
        return self.ans
