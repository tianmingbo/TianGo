# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 16:25
# @Author  : tmb
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root:
            return root
        if root.val > p.val and root.val > q.val:  # 如果当前值大于p,q的值，说明在此节点的left
            left = self.lowestCommonAncestor(root.left, p, q)
            return left
        if root.val < p.val and root.val < q.val:  # 在当前节点的右边
            right = self.lowestCommonAncestor(root.right, p, q)
            return right
        # 如果不存在上述情况，说明当前节点就是公共祖先
        return root
