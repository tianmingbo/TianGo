#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author bo~
@Date 2023/3/4 18:05
@Describe 二维动态规划，首尾拿石子
核心思路为：dp[i][j] 表示左指针为i，右指针为j的数组中，先手的人能赢几分，（就是自己抢的最多值 - 对手抢的最多值）
"""
from typing import List


class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        length = len(piles)
        dp = [[0] * length for _ in range(length)]  # 存储先手和后手的值的 差值
        for i in range(length - 1, -1, -1):
            for j in range(i + 1, length):
                if i == j:
                    # base case, 先手完胜
                    dp[i][j] = piles[i]
                    continue

                dp[i][j] = max(piles[i] - dp[i + 1][j], piles[j] - dp[i][j - 1])
        return dp[0][length - 1] > 0


if __name__ == '__main__':
    a = Solution()
    print(a.stoneGame([2, 8, 3, 5]))
