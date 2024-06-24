# -*- coding: utf-8 -*-
# @Time    : 2020/9/29 10:02
# @Author  : tmb
'''
层次遍历，把每一层的串起来
'''


class Solution:
    def connect(self, root):
        if not root:
            return root

        def bfs(curlayer):
            nextlayer = []
            for i in curlayer:
                if i.left:
                    nextlayer.append(i.left)
                if i.right:
                    nextlayer.append(i.right)
            if len(nextlayer) > 1:
                for j in range(0, len(nextlayer) - 1):
                    nextlayer[j].next = nextlayer[j + 1]
            if nextlayer:
                bfs(nextlayer)

        bfs([root])
        return root
