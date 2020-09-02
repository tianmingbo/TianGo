# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 10:45
# @Author  : tmb

# 递归，始终保持左子树小于父结点，右子树大于父结点
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    # 中序遍历，递增
    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        stack, inorder = [], float('-inf')

        while stack or root:
            while root:
                stack.append(root)
                root = root.left
            root = stack.pop()
            # 如果中序遍历得到的节点的值小于等于前一个 inorder，说明不是二叉搜索树
            if root.val <= inorder:
                return False
            inorder = root.val
            root = root.right

        return True


# 🐼


class Solution2:
    def isValidBST(self, root) -> bool:

        # def dfs(node, min_val, max_val):
        #     if not node:  # 边界条件，如果node为空肯定是二叉搜索树
        #         return True
        #     if not min_val < node.val < max_val:  # 如果当前节点超出上下界范围，肯定不是
        #         return False
        #     # 走到下面这步说明已经满足了如题所述的二叉搜索树的前两个条件
        #     # 那么只需要递归判断当前节点的左右子树是否同时是二叉搜索树即可
        #     return dfs(node.left, min_val, node.val) and dfs(node.right, node.val, max_val)
        #
        # return dfs(root, float('-inf'), float('inf'))  # 对于根节点，它的上下限为无穷大和无穷小
        def dfs(node, min_val, max_val):
            if not node:
                return True
            if not min_val < node.val < max_val:
                return False
            if not dfs(node.left, min_val, node.val):
                return False
            if not dfs(node.right, node.val, max_val):
                return False
            return True

        return dfs(root, float('-inf'), float('inf'))


class Solution3:
    def isValidBST(self, root):
        """
        同2，好理解
        :type root: TreeNode
        :rtype: bool
        """

        def helper(node, lower=float('-inf'), upper=float('inf')):
            if not node:
                return True

            val = node.val
            if val <= lower or val >= upper:
                return False

            if not helper(node.right, val, upper):
                return False
            if not helper(node.left, lower, val):
                return False
            return True

        return helper(root)
