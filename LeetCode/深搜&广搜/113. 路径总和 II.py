# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 14:10
# @Author  : tmb

from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def pathSum(self, root: TreeNode, sum1: int) -> List[List[int]]:
        if not root:
            return []
        res = []

        def dfs(root, path):
            path.append(root.val)
            if not root.left and not root.right:
                if sum(path) == sum1:
                    res.append(path[:])
            if root.left:
                dfs(root.left, path)
                path.pop()
            if root.right:
                dfs(root.right, path)
                path.pop()

        dfs(root, [])
        return res
