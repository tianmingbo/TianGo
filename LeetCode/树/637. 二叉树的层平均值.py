# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 20:47
# @Author  : tmb
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


'''
层序遍历
'''


class Solution:
    def averageOfLevels(self, root: TreeNode) -> List[float]:
        if not root:
            return []
        queue = [root]
        res = []
        while queue:
            count, sum_node, tmp = 0, 0, []
            for _ in range(len(queue)):
                node = queue.pop(0)
                count += 1
                sum_node += node.val
                if node.left:
                    tmp.append(node.left)
                if node.right:
                    tmp.append(node.right)
            queue = tmp[:]
            res.append(sum_node / count)
        return res
