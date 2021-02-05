# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 19:40
# @Author  : tmb
class Solution:
    def numSquares(self, n: int) -> int:
        if not n:
            return 0
        dp = [n+1 for _ in range(n + 1)]
        tmp = int(n ** 0.5) + 1
        tmp = [i ** 2 for i in range(1, tmp + 1)]
        dp[0], dp[1] = 0, 1
        for j in range(1, n + 1):
            for i in tmp:
                if j < i:  # 小于tmp中的最大值，已经到边界了
                    break
                dp[j] = min(dp[j], dp[j - i] + 1)  # 和金币兑换相似
        return dp[n]


if __name__ == '__main__':
    a = Solution()
    print(a.numSquares(96))
