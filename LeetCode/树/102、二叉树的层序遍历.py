# -*- coding: utf-8 -*-
# @Time    : 2020/9/3 9:35
# @Author  : tmb

# 使用队列进行层序遍历
class Solution:
    def levelOrder(self, root):
        if not root:
            return []
        queue = [root]
        res = []
        while queue:
            level = []
            n = len(queue)
            for _ in range(n):  # 第n层，都出队列，把n+1层的子结点加入队列（如果存在的话）
                tmp = queue.pop(0)
                level.append(tmp.val)
                if tmp.left:
                    queue.append(tmp.left)
                if tmp.right:
                    queue.append(tmp.right)
            res.append(level)
        return res
