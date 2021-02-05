# -*- coding: utf-8 -*-
# @Time    : 2020/10/9 11:35
# @Author  : tmb
'''
并查集使用：有多少朋友圈|属于谁|任给两个人，是不是朋友
'''


# 类似岛屿问题，可以使用dfs，bfs，也可以使用并查集

class Solution:
    def findCircleNum(self, M) -> int:
        if not M:
            return 0
        n = len(M)
        p = [i for i in range(n)]  # 初始化并查集
        for i in range(n): #创建并查集
            for j in range(n):
                if M[i][j] == 1:
                    self.union(p, i, j)
                    print(p)
        a = set([self.parent(p, i) for i in range(n)])  # [1,2,2] 关系具有传递性，0和1是朋友，1和2是朋友，所以0和2是朋友，判断有几个孤立的群
        return len(a)

    def union(self, p, i, j):
        p1 = self.parent(p, i)
        p2 = self.parent(p, j)
        p[p1] = p2

    def parent(self, p, i):
        root = i
        while p[root] != root:
            root = p[root]
        while p[i] != i:  # 路径压缩，可以不做压缩
            x = i
            i = p[i]
            p[x] = root
        return root


if __name__ == '__main__':
    a = Solution()
    b = a.findCircleNum([[1, 1, 0],
                         [1, 1, 1],
                         [0, 1, 1]])
    print(b)
