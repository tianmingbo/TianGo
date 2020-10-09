# -*- coding: utf-8 -*-
# @Time    : 2020/10/9 10:31
# @Author  : tmb
class DistictSet(object):
    def __init__(self, n):
        self.p = [i for i in range(n)]

    def parent(self, p, i):
        root = i
        while p[root] != root:
            root = p[root]
        while p[i] != i:
            x = i
            i = p[i]
            p[x] = root
        return root

    def union(self, p, i, j):
        p1 = self.parent(p, i)
        p2 = self.parent(p, j)
        p[p1] = p2


if __name__ == '__main__':
    a = DistictSet(4)
    print(a.parent(a.p, 1))
    print(a.p)
