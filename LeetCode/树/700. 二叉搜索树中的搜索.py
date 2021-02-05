# -*- coding: utf-8 -*-
# @Time    : 2020/12/26 20:08
# @Author  : tmb
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def searchBST(self, root: TreeNode, val: int) -> TreeNode:
        if not root or root.val == val:
            return root
        if val < root.val:
            return self.searchBST(root.left, val)  # 搜索到目标值了，就立马return
        if val > root.val:
            return self.searchBST(root.right, val)

        return None

    def searchBST2(self, root: TreeNode, val: int) -> TreeNode:
        while root:
            if root.val > val:
                root = root.left
            elif root.val < val:
                root = root.right
            else:
                return root
        return None
