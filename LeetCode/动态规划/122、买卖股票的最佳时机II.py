# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 10:58
# @Author  : tmb


'''
二维，第一维表示天数，第二维表示手里是现金还是股票
 第i天手里是现金，判断第(i-1)天 现金和把股票卖掉 哪个收益高
 第i天手里是股票，分为：第i-1天手里是现金，然后买入股票，以及本来就持有股票两种情况
'''


class Solution:
    def maxProfit(self, prices):
        if len(prices) < 2:
            return 0
        dp = [[0, 0] for _ in range(len(prices))]
        dp[0][0] = 0  # 第一天手里是现金
        dp[0][1] = -prices[0]  # 第一天手里是股票
        for i in range(1, len(prices)):
            dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])
            dp[i][1] = max(dp[i - 1][0] - prices[i], dp[i - 1][1])
        return dp[-1][0]


class Solution2:
    def maxProfit(self, prices):
        '''
        今天比昨天高就卖出，这是当买卖次数不受限制的时候
        :param prices:
        :return:
        '''
        if len(prices) < 2:
            return 0
        # max = 0
        # for i in range(1, len(prices)):
        #     if prices[i] > prices[i - 1]:
        #         max += prices[i] - prices[i - 1]
        # return max
        return sum(max(prices[i + 1] - prices[i], 0) for i in range(len(prices) - 1))


if __name__ == '__main__':
    a = Solution2()
    print(a.maxProfit([7, 15, 5, 3, 6, 4]))
