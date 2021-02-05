# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 14:45
# @Author  : tmb

class Solution:
    def maxProfit(self, prices) -> int:
        if not prices:
            return 0
        dp = [[0, 0] for _ in prices]
        for i in range(len(prices)):
            if i - 1 == -1:
                dp[i][0] = 0
                # dp[0][0]=max(dp[-1][0],dp[-1][1]+prices[i])=0
                dp[i][1] = -prices[i]
                # dp[i][1]=max(dp[0][1],dp[0][0]-prices[i])=-prices[i]
                continue
            dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])
            dp[i][1] = max(dp[i - 1][1], - prices[i])
        return dp[-1][0]


'''
dp[i][k][0]:第i天没有持有股票
dp[i][k][1]:第i天持有股票
dp[i][k][0]= max(dp[i-1][k][0] , dp[i-1][k][1] + prices[i]) :第i天没有持有股票的最大值是
                 i-1天保持不变      i-1天持有，并卖出
dp[i][k][1] = max(dp[i-1][k][1] , dp[i-1][k-1][0]- prices[i]) :第i天持有股票的最大值是
                   i-1天保持不变      i-1天没有，买入
临界条件：
dp[-1][k][0] = 0   从第0天开始，-1天没有值
dp[-1][k][1] = -float('inf') -1天持有股票，不可能存在
dp[i][0][0] = 0  没有交易次数，值为0
dp[i][0][1] = -float('inf') 没有交易次数，却持有股票，不可能存在
'''

if __name__ == '__main__':
    a = Solution()
    print(a.maxProfit([7, 1, 5, 3, 6, 4]))
