# -*- coding: utf-8 -*-
# @Time    : 2020/9/12 10:40
# @Author  : tmb
class Solution:
    def maxProfit(self, prices) -> int:
        if not prices:
            return 0
        max_value = 0
        for i in range(len(prices) - 1, 0, -1):
            if prices[i] > prices[i - 1]:
                max_value += prices[i] - prices[i - 1]
        return max_value


if __name__ == '__main__':
    a = Solution()
    print(a.maxProfit([7, 6, 4, 3, 1]))
