# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 11:19
# @Author  : tmb
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            # 递归终止条件
            return 0

        # 当前层逻辑
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        return 1 + max(left_depth, right_depth)
