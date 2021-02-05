# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 20:03
# @Author  : tmb
from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        dp = [0 for _ in range(amount + 1)]
        dp[0] = 1
        for coin in coins:
            for j in range(coin, amount + 1):
                dp[j] = dp[j] + dp[j - coin]
            print(dp)
            '''
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0] #全用金币2
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 2, 1] #用金币2,5
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 1] #用金币2,5,10
            '''
        return dp[amount]


if __name__ == '__main__':
    a = Solution()
    print(a.change(amount=11, coins=[2, 5, 10]))
