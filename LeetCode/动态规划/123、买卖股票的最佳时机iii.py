# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 11:28
# @Author  : tmb
from typing import List


# dp[i][k][0],dp[i][k][1]

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        # 不能[[[0] * 2 ]*3  for _ in range(len(prices))] 简历dp table，存在浅复制的bug
        dp = [[[0] * 2 for _ in range(3)] for _ in range(len(prices))]
        for i in range(len(prices)):
            for j in range(2, 0, -1):
                if i - 1 == -1:
                    dp[-1][j][0] = 0
                    dp[-1][j][1] = -float('inf')
                if j - 1 == 0:
                    dp[i][0][0] = 0
                    dp[i][0][1] = -float('inf')

                dp[i][j][0] = max(dp[i - 1][j][0], dp[i - 1][j][1] + prices[i])
                dp[i][j][1] = max(dp[i - 1][j][1], dp[i - 1][j - 1][0] - prices[i])

        return dp[-1][2][0]


if __name__ == '__main__':
    a = Solution()
    print(a.maxProfit([3, 3, 5, 0, 0, 3, 1, 4]))
