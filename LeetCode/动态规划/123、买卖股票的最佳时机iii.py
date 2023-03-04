# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 11:28
# @Author  : tmb
import math
from typing import List


# dp[i][k][0],dp[i][k][1]

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        dp = [[[0] * 2 for _ in range(3)] for _ in range(len(prices))]
        for i in range(len(prices)):
            for k in range(2, 0, -1):  # 倒序，k的次数是逐渐变小的
                if i - 1 == -1:
                    dp[i][k][0] = 0
                    dp[i][k][1] = -prices[i]
                    continue

                dp[i][k][0] = max(dp[i - 1][k][0], dp[i - 1][k][1] + prices[i])
                dp[i][k][1] = max(dp[i - 1][k][1], dp[i - 1][k - 1][0] - prices[i])

        return dp[-1][2][0]


if __name__ == '__main__':
    a = Solution()
    print(a.maxProfit([3, 3, 5, 0, 0, 3, 1, 4]))
