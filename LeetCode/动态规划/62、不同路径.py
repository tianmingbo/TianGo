# -*- coding: utf-8 -*-
# @Time    : 2020/9/4 16:14
# @Author  : tmb

# 思路,从左下角开始走
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):  # 处理最后一列
            dp[i][m - 1] = 1
        for j in range(m):  # 处理最后一行
            dp[n - 1][j] = 1
        for raw in range(n - 2, -1, -1):  # 主逻辑，从下往上，当前元素有两种可能（下边的和右边的），都加上
            for col in range(m - 2, -1, -1):
                dp[raw][col] = dp[raw + 1][col] + dp[raw][col + 1]
        return dp[0][0]


if __name__ == '__main__':
    a = Solution()
    print(a.uniquePaths(7, 3))
