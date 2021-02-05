# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 17:14
# @Author  : tmb
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


'''
中序遍历就是递增的，要想保持平衡，每次取中间的，必定平衡
'''


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> TreeNode:
        def dfs(left, right):
            if left > right:
                return None
            mid = (left + right) >> 1
            root = TreeNode(nums[mid])
            root.left = dfs(left, mid - 1)
            root.right = dfs(mid + 1, right)
            return root

        return dfs(0, len(nums) - 1)


if __name__ == '__main__':
    a = Solution()
    a.sortedArrayToBST([-10, -3, 0, 5, 9])
