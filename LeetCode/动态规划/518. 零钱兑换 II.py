# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 20:03
# @Author  : tmb
from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        n = len(coins)
        dp = [0] * (amount + 1)
        dp[0] = 1

        for i in range(1, n + 1):
            for j in range(1, amount + 1):
                if j - coins[i - 1] >= 0:
                    dp[j] = dp[j] + dp[j - coins[i - 1]]
                    print(i, j, dp)
            # print(dp)
        return dp[amount]


if __name__ == '__main__':
    a = Solution()
    print(a.change(amount=5, coins=[1, 2, 5]))
