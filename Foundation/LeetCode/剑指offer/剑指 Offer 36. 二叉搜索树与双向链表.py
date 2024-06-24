# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 17:40
# @Author  : tmb

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:

    def __init__(self):
        self.head = None
        self.pre = None

    def treeToDoublyList(self, root: 'Node') -> 'Node':
        if not root:
            return root

        def helper(node):
            # 中序遍历
            if not node:
                return
            helper(node.left)  # 实质是中序遍历
            if self.pre:
                self.pre.right, node.left = node, self.pre  # 构建双向指针
            else:
                self.head = node  # 保存头结点
            self.pre = node  # 每次后移
            helper(node.right)

        helper(root)
        self.head.left, self.pre.right = self.pre, self.head  # 做最后处理，处理头结点和尾结点
        return self.head
