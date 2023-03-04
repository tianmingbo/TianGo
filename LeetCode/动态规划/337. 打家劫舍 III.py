# -*- coding: utf-8 -*-
# @Time    : 2020/12/6 14:49
# @Author  : tmb
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    memo = {}

    def rob(self, root: TreeNode) -> int:
        if root in self.memo:
            return self.memo[root]
        if not root:
            return 0
        # 抢了后去下下家
        do_it = root.val
        if root.left:
            do_it += self.rob(root.left.left)
            do_it += self.rob(root.left.right)
        if root.right:
            do_it += self.rob(root.right.left)
            do_it += self.rob(root.right.right)
        # 不抢，去下家看看
        not_do = self.rob(root.left) + self.rob(root.right)
        res = max(do_it, not_do)
        self.memo[root] = res
        return res
