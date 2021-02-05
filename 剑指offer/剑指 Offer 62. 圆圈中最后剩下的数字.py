# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 19:46
# @Author  : tmb
class Solution:
    def lastRemaining(self, n: int, m: int) -> int:
        f = 0
        for i in range(2, n + 1):
            f = (m + f) % i
        return f


if __name__ == '__main__':
    a = Solution()
    print(a.lastRemaining(n=5, m=3))
