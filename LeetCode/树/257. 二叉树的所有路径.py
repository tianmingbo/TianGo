# -*- coding: utf-8 -*-
# @Time    : 2020/12/26 17:19
# @Author  : tmb
# Definition for a binary tree node.
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def binaryTreePaths(self, root: TreeNode) -> List[str]:
        if not root:
            return []
        res = []

        def dfs(root, path):
            path.append(root.val)  # 实质前序遍历
            if not root.left and not root.right:  # 回溯终止条件
                res.append(path[:])
            if root.left:  # 左
                dfs(root.left, path)
                path.pop()
            if root.right:  # 右
                dfs(root.right, path)
                path.pop()

        dfs(root, [])
        return ['->'.join([str(j) for j in i]) for i in res]
