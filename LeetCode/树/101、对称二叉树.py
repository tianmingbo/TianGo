# -*- coding: utf-8 -*-
# @Time    : 2020/9/3 11:47
# @Author  : tmb
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    def isSymmetric(self, root) -> bool:
        if not root:
            return True

        def dfs(left, right):
            if not left and not right:  # 左右结点都为空，True
                return True
            if left and right and left.val == right.val:  # 左右结点同时存在且值相等
                return dfs(left.left, right.right) and dfs(left.right, right.left)
            return False

        return dfs(root.left, root.right)


class Solution2:
    def isSymmetric(self, root):
        if root is None:
            return True

        stack = [[root.left, root.right]]
        while len(stack) > 0:
            pair = stack.pop(0)
            left = pair[0]
            right = pair[1]

            if left is None and right is None:
                continue
            if left is None or right is None:
                return False
            if left.val == right.val:
                stack.insert(0, [left.left, right.right])

                stack.insert(0, [left.right, right.left])
            else:
                return False
        return True
