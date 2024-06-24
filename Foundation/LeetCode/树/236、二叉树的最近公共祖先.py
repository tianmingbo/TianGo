# -*- coding: utf-8 -*-
# @Time    : 2020/9/29 10:33
# @Author  : tmb
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root or p == root or q == root:  # 终止条件，如果root为空，或者root=q | root=q
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:  # left和right都不为空，说明当前root就是最近公共祖先
            return root
        return left or right  # left为空，或者right为空，就返回对应子树


class Solution2:
    '''
     o1, o2是val的情况下
    '''

    def lowestCommonAncestor(self, root, o1, o2):
        if not root:
            return
        if o1 == root.val:
            return o1
        if o2 == root.val:
            return o2
        left = self.lowestCommonAncestor(root.left, o1, o2)
        right = self.lowestCommonAncestor(root.right, o1, o2)
        if left and right:
            return root.val
        return left or right
