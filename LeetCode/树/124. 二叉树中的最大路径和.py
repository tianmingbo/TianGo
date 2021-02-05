# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 20:01
# @Author  : tmb
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    res = -1e9

    # 解释：以 -10，-9,20为例
    def maxPathSum(self, root: TreeNode) -> int:
        def helper(node):
            if not node:  # 如果没有左右节点，返回为0
                return 0
            left_devote = max(helper(node.left), 0)  # 向左节点遍历，-9向上返回的为0
            right_devote = max(helper(node.right), 0)  # 向右节点递归，20返回的值为20，  根节点最大值为10，小于20
            self.res = max(self.res, node.val + left_devote + right_devote)  # res为20
            return node.val + max(left_devote, right_devote)  # -9 向上返回的为-9

        helper(root)
        return self.res
