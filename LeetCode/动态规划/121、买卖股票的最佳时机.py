# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 14:45
# @Author  : tmb
'''
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/solution/yi-ge-fang-fa-tuan-mie-6-dao-gu-piao-wen-ti-by-l-3/
'''
class Solution:
    def maxProfit(self, prices) -> int:
        if not prices:
            return 0
        dp = [[0, 0] for _ in prices]
        for i in range(len(prices)):
            if i - 1 == -1:
                dp[i][0] = 0
                dp[i][1] = -prices[i]
                continue
            dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])
            dp[i][1] = max(dp[i - 1][1], - prices[i])
        return dp[-1][0]


if __name__ == '__main__':
    a = Solution()
    print(a.maxProfit([7, 1, 5, 3, 6, 4]))
