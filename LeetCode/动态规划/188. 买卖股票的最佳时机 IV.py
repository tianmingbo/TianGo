# -*- coding: utf-8 -*-
# @Time    : 2020/12/2 21:54
# @Author  : tmb
from typing import List


class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        if not prices:
            return 0
        dp = [[[0] * 2 for _ in range(k + 1)] for _ in range(len(prices))]
        for i in range(len(prices)):
            for j in range(k, 0, -1):
                if i - 1 == -1:
                    dp[-1][j][0] = 0
                    dp[-1][j][1] = -float('inf')
                if j - 1 == 0:
                    dp[i][0][0] = 0
                    dp[i][0][1] = -float('inf')
                dp[i][j][0] = max(dp[i - 1][j][0], dp[i - 1][j][1] + prices[i])
                dp[i][j][1] = max(dp[i - 1][j][1], dp[i - 1][j - 1][0] - prices[i])
        return dp[-1][k][0]


if __name__ == '__main__':
    a = Solution()
    print(a.maxProfit(k=2, prices=[3, 2, 6, 5, 0, 3]))
