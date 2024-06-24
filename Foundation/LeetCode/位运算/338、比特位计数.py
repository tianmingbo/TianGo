# -*- coding: utf-8 -*-
# @Time    : 2020/10/14 10:03
# @Author  : tmb
class Solution:
    def countBits(self, num: int):
        dp = [_ for _ in range(num + 1)]
        dp[0] = 0
        for i in range(1, num + 1):
            dp[i] = dp[(i & (i - 1))] + 1  # 动态规划，O（n）时间、空间复杂度
        return dp


if __name__ == '__main__':
    a = Solution()
    a.countBits(3)
