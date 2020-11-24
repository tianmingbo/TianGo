# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 17:41
# @Author  : tmb
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


'''
输入：root = [1,3,null,null,2]
输出：[3,1,null,null,2]
'''


class Solution(object):
    def recoverTree(self, root):
        self.wrong_1 = None
        self.wrong_2 = None
        self.pre = None

        def dfs(root):
            if not root:
                return
            dfs(root.left)  # 中序遍历是递增的，如果不是递增，说明这个就是错误结点
            if not self.pre:
                self.pre = root
            else:
                if self.pre.val > root.val:  # 前一个大于后一个，出错
                    self.wrong_2 = root  # 第二个出错的结点
                    if not self.wrong_1:  # 记录第一个出错的结点
                        self.wrong_1 = self.pre
                self.pre = root
            dfs(root.right)

        dfs(root)
        if self.wrong_1 and self.wrong_2:  # 如果找到出错的两个结点了，则交换值
            self.wrong_1.val, self.wrong_2.val = self.wrong_2.val, self.wrong_1.val
