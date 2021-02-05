# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 16:43
# @Author  : tmb
from typing import List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    '''
    实质是前序遍历
    '''

    def pathSum(self, root: TreeNode, sum1: int) -> List[List[int]]:
        if not root:
            return []
        res = []

        def helper(node, path):
            path.append(node.val)
            if sum(path) == sum1 and not (node.left or node.right):
                res.append(path[:])
            if node.left:
                helper(node.left, path)
                path.pop()
            if node.right:
                helper(node.right, path)
                path.pop()

        helper(root, [])
        return res
