# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 17:31
# @Author  : tmb
from typing import List


# 没有看懂
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

    def findMaxForm1(self, strs: List[str], m: int, n: int) -> int:
        # m个0，n个1
        dp = [[[0] * (n + 1) for _ in range(m + 1)] for _ in range(len(strs) + 1)]
        for i in range(1, len(strs) + 1):  # 两种状态，三次循环， strs选不选
            z, o = self.count(strs[i - 1])
            for j in range(m + 1):  # 1的数量
                for k in range(n + 1):  # 0的数量
                    if j >= z and k >= o:
                        dp[i][j][k] = max(dp[i - 1][j][k],
                                          dp[i - 1][j - z][k - o] + 1)  # dp[i - 1][j - z][k - o] + 1 消费z个1，o个0，计数加1
                    else:
                        dp[i][j][k] = dp[i - 1][j][k]
        return dp[-1][-1][-1]

    def count(self, s):
        return sum(1 for c in s if c == '0'), sum(1 for c in s if c == '1')

    # 优化一下下

    def findMaxForm3(self, strs: List[str], m: int, n: int) -> int:
        if len(strs) == 0:
            return 0
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for strs_item in strs:
            zeros, ones = self.count(strs_item)
            for i in range(m, zeros - 1, -1):
                for j in range(n, ones - 1, -1):
                    dp[i][j] = max(dp[i][j], 1 + dp[i - zeros][j - ones])
        return dp[m][n]


if __name__ == '__main__':
    a = Solution()
    print(a.findMaxForm3(strs=["10", "0001", "111001", "1", "0"], m=5, n=3))
