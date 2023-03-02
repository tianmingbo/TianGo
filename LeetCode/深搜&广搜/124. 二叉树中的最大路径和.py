# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
import math


class Solution:
    def __init__(self):
        self.max_sum = -math.inf

    def maxPathSum(self, root) -> int:
        def dfs(root):
            if not root:
                return 0
            left = dfs(root.left)
            right = dfs(root.right)
            self.max_sum = max(self.max_sum, left + right + root.val)
            return max(0, max(left, right) + root.val)

        dfs(root)
        return self.max_sum
