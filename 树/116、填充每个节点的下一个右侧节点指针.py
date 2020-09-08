# -*- coding: utf-8 -*-
# @Time    : 2020/9/4 14:56
# @Author  : tmb
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


'''
使用常数级空间，没有想法。使用层序遍历，空间复杂度O(n)
'''


class Solution:
    def connect(self, root):
        if not root:
            return root
        pre = root
        # 当只用根结点or所有层都已遍历
        while pre.left:
            tmp = pre
            while tmp:
                tmp.left.next = tmp.right  # 串联左子树和右子树
                if tmp.next:  # 当为根结点时，不通过
                    tmp.right.next = tmp.next.left  # 串联两个不是兄弟结点的结点
                tmp = tmp.next  # 继续右边遍历
            pre = pre.left  # 从下一层的最左边开始
        return root
