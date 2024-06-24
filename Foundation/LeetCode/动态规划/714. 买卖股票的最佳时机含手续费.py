# -*- coding: utf-8 -*-
# @Time    : 2020/12/2 20:53
# @Author  : tmb
from typing import List


class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        if not prices:
            return 0
        dp = [[0] * 2 for _ in range(len(prices))]
        dp[0][0] = 0
        dp[0][1] = -prices[0] - fee  # 第0天买入扣2块钱手续费
        for i in range(1, len(prices)):
            dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])
            dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - prices[i] - fee)  # 每次买入的时候减去费用
        return dp[-1][0]


if __name__ == '__main__':
    a = Solution()
    print(a.maxProfit(prices=[1, 3, 2, 8, 4, 9], fee=2))
