# 组团 配对 问题
class DistictSet(object):
    def __init__(self, n):  # 初始化，自己指向自己
        self.p = [i for i in range(n)]

    def parent(self, p, i):
        root = i
        while p[root] != root:  # 是不是等于自身
            root = p[root]
        while p[i] != i:  # 路径压缩可以不做
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
