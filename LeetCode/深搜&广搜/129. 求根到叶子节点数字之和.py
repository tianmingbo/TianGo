# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 11:05
# @Author  : tmb
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def sumNumbers(self, root: TreeNode) -> int:
        if not root:
            return 0
        sum_path = []

        def dfs(root, path):
            path.append(str(root.val))  # 当成字符串处理，整型不好搞
            if not root.left and not root.right:
                sum_path.append(''.join(path[:]))
            if root.left:
                dfs(root.left, path)
            if root.right:
                dfs(root.right, path)
            path.pop()

        dfs(root, [])
        return sum([int(i) for i in sum_path])
