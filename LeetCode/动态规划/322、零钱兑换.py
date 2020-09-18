# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 16:59
# @Author  : tmb

# 时间复杂度O(n^2)，空间复杂度O(n)
class Solution:
    def coinChange(self, coins, amount: int) -> int:
        # 我的解法
        if not coins:
            return -1
        if not amount:
            return 0
        coins.sort()  # 钢镚面值排序 O(logn)
        dp = [float('inf') for _ in range(amount + 1)]
        use_coins = []  # 已经使用过的钢镚
        if coins[0] > amount:  # 如果要兑换的钱的面值，比钢镚的最小值还小，那么没有值可以兑换
            return -1
        for i in range(coins[0], amount + 1):  # O(n^2)
            if i in coins:
                use_coins.append(i)
                dp[i] = 1  # 正好可以兑换，dp[i]赋值为1
            else:
                for j in use_coins:  # 如钢镚[1,2],则3可以由1和2得到，6由5,2,1得到
                    dp[i] = min(dp[i], dp[i - j] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1


class Solution2:
    def coinChange(self, coins, amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            for x in range(coin, amount + 1):
                dp[x] = min(dp[x], dp[x - coin] + 1)
                print(dp)
        return dp[amount] if dp[amount] != float('inf') else -1


if __name__ == '__main__':
    a = Solution()
    print(a.coinChange([1, 2, 5], amount=11))
