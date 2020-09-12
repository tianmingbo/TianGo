# -*- coding: utf-8 -*-
# @Time    : 2020/9/11 16:52
# @Author  : tmb
# 层次遍历，广度优先
class Solution:
    def largestValues(self, root):
        if not root:
            return
        res = []
        queue = [root]
        while queue:
            level_tmp = []
            n = len(queue)
            for i in range(n):
                tmp = queue.pop(0)
                level_tmp.append(tmp.val)
                if tmp.left:
                    queue.append(tmp.left)
                if tmp.right:
                    queue.append(tmp.right)
            res.append(max(level_tmp))
        return res

# if __name__ == '__main__':
#     a=Solution()
#     a.largestValues()
