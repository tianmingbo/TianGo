# -*- coding: utf-8 -*-
# @Time    : 2020/9/4 10:24
# @Author  : tmb
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def buildTree(self, inorder, postorder):
        # 实际上inorder 和 postorder一定是同时为空的，因此你无论判断哪个都行
        if not inorder:
            return None
        root = TreeNode(postorder[-1])
        i = inorder.index(root.val)
        root.left = self.buildTree(inorder[:i], postorder[:i])
        root.right = self.buildTree(inorder[i + 1:], postorder[i:-1])
        return root


if __name__ == '__main__':
    a = Solution()
    b = a.buildTree([9, 3, 15, 20, 7], [9, 15, 7, 20, 3])
