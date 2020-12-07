# -*- coding: utf-8 -*-
# @Time    : 2020/12/7 16:58
# @Author  : tmb
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def constructMaximumBinaryTree(self, nums: List[int]) -> TreeNode:
        if not nums:
            return
        if len(nums) == 1:
            return TreeNode(nums[0])
        cur_node_val = max(nums)  # 根的值
        root = TreeNode(cur_node_val)
        index = nums.index(cur_node_val)  # 最大值的索引
        root.left = self.constructMaximumBinaryTree(nums[:index])
        root.right = self.constructMaximumBinaryTree(nums[index + 1:])
        return root
