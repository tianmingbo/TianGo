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
        if len(nums) == 1:  # 长度为1，终止条件
            return TreeNode(nums[0])
        cur_node_val = max(nums)  # 根的值
        root = TreeNode(cur_node_val)
        index = nums.index(cur_node_val)  # 最大值的索引，题目已知值唯一
        if index > 0:  # 确保左子树至少有一个
            root.left = self.constructMaximumBinaryTree(nums[:index])
        if index < len(nums) - 1:  # 确保右子树至少有一个
            root.right = self.constructMaximumBinaryTree(nums[index + 1:])
        return root
