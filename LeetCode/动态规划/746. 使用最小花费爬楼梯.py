# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 19:24
# @Author  : tmb
from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        dp = [0 for _ in range(len(cost))]
        dp[0], dp[1] = cost[0], cost[1]
        for i in range(2, len(cost)):
            dp[i] = min((dp[i - 1] + cost[i]), (dp[i - 2] + cost[i]))
        return min(dp[-1], dp[-2])


if __name__ == '__main__':
    a = Solution()
    print(a.minCostClimbingStairs(cost=[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]))
