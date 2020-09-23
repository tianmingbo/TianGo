# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 11:28
# @Author  : tmb
class Solution:
    def maxProfit(self, prices) -> int:
        if not prices:
            return 0
        dp = [[[0, 0] for _ in range(3)] for _ in prices]

        print(dp)
        # print(dp[0][1][1])
        # for i in range(len(prices)):
        #     for j in range(1, 3):
        #         if i - 1 == -1:
        #             dp[i][2][0] = 0
        #             dp[i][2][1] = -float('inf')
        #             continue
        #         dp[i][j][0] = max(dp[i - 1][j][0], dp[i - 1][j][1] + prices[i])
        #         dp[i][j][1] = max(dp[i - 1][j][1], dp[i - 1][j - 1][0] - prices[i])

        dp_i10 = 0
        dp_i11 = -float('inf')

        dp_i20 = 0
        dp_i21 = -float('inf')
        for price in prices:
            dp_i20 = max(dp_i20, dp_i21 + price)
            dp_i21 = max(dp_i21, dp_i10 - price)
            dp_i10 = max(dp_i10, dp_i11 + price)
            dp_i11 = max(dp_i11, -price)

        return dp_i20


if __name__ == '__main__':
    a = Solution()
    print(a.maxProfit([3, 3, 5, 0, 0, 3, 1, 4]))
