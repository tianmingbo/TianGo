# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 20:33
# @Author  : tmb
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def flatten(self, root: TreeNode) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        all_node = []

        def dfs(root):  # 前序遍历
            if not root:
                return
            all_node.append(root)
            dfs(root.left)
            dfs(root.right)

        dfs(root)
        for i in range(1, len(all_node)):  # 对结点进行处理
            pre = all_node[i - 1]
            cur = all_node[i]
            pre.left = None
            pre.right = cur

    def flatten2(self, root):
        if not root:
            return
        self.flatten2(root.left)
        self.flatten2(root.right)

        left = root.left
        right = root.right
        root.left = None
        root.right = left

        p = root
        while p.right is not None:
            p = p.right
        p.right = right
