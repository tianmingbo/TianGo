# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 17:31
# @Author  : tmb
from typing import List

#没有看懂
class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        def count(s):
            return sum(1 for c in s if c == '0'), sum(1 for c in s if c == '1')

        for z, o in [count(s) for s in strs]:
            for x in range(m, -1, -1):
                for y in range(n, -1, -1):
                    if x >= z and y >= o:
                        dp[x][y] = max(1 + dp[x - z][y - o], dp[x][y])

        return dp[m][n]


if __name__ == '__main__':
    a = Solution()
    print(a.findMaxForm(strs=["10", "0001", "111001", "1", "0"], m=5, n=3))
