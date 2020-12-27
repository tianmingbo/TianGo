# -*- coding: utf-8 -*-
# @Time    : 2020/12/26 16:52
# @Author  : tmb
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


'''
可以使用层序和递归方式遍历
'''


class Solution:
    def countNodes(self, root: TreeNode) -> int:
        if not root:
            return 0  # 返回0，表示个数为0
        left_num = self.countNodes(root.left)
        right_num = self.countNodes(root.right)
        return 1 + left_num + right_num  # 加1是为了加上根节点

    def countNodes2(self, root: TreeNode) -> int:
        if not root:
            return 0
        queue = [root]
        res = []
        while queue:
            tmp = queue.pop(0)
            if tmp.left:
                queue.append(tmp.left)
            if tmp.right:
                queue.append(tmp.right)
        return len(res)
