# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 16:43
# @Author  : tmb
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def insertIntoBST(self, root: TreeNode, val: int) -> TreeNode:
        if not root:
            return TreeNode(val)
        self.build(root, val)
        return root

    def build(self, root, val):
        while root:
            if root.val > val:
                if not root.left:  # 见缝插针
                    root.left = TreeNode(val)
                    return
                else:
                    root = root.left
            elif root.val < val:
                if not root.right:
                    root.right = TreeNode(val)
                    return
                else:
                    root = root.right
