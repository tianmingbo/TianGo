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
        def helper(root):
            if root in self.memo:
                return self.memo[root]
            if not root:
                return 0
            # just_do_it = root.val
            # if root.left:
            #     just_do_it += self.rob(root.left.left)
            #     just_do_it += self.rob(root.left.right)
            # if root.right:
            #     just_do_it += self.rob(root.right.left)
            #     just_do_it += self.rob(root.right.right)
            just_do_it = root.val + (0 if not root.left else self.rob(root.left.left) + self.rob(root.left.right)) + (
                0 if not root.right else self.rob(root.right.left) + self.rob(root.right.right))
            a_little_scared = self.rob(root.left) + self.rob(root.right)
            res = max(just_do_it, a_little_scared)
            self.memo[root] = res
            return res

        return helper(root)
