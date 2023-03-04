# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 20:03
# @Author  : tmb
from typing import List


# 完全背包问题，每个物体的数量不限

class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        n = len(coins)
        dp = [[0] * (amount + 1) for _ in range(n + 1)]  # 一维，硬币，二维，硬币可以组成的金额
        for k in range(n + 1):  # 临界条件，当需要拼的金额为0是，有1种
            dp[k][0] = 1
        # print(dp)
        for i in range(1, n + 1):  # 金币
            for j in range(1, amount + 1):  # 拼成的金额
                if j - coins[i - 1] < 0:
                    dp[i][j] = dp[i - 1][j]
                else:
                    '''
                    如果你不把这第i个物品装入背包，也就是说你不使用coins[i]这个面值的硬币，那么凑出面额j的方法数dp[i][j]应该等于dp[i-1][j]，继承之前的结果。
                    如果你把这第i个物品装入了背包，也就是说你使用coins[i]这个面值的硬币，那么dp[i][j]应该等于dp[i][j-coins[i-1]]。
                    '''
                    dp[i][j] = dp[i - 1][j] + dp[i][j - coins[i - 1]]
        return dp[n][amount]


if __name__ == '__main__':
    a = Solution()
    print(a.change(amount=6, coins=[1, 2, 5]))
