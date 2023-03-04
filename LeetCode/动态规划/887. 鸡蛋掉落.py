#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/3/4 20:21
    @Describe 
"""


class Solution:
    def superEggDrop(self, k: int, n: int):

        memo = dict()

        def dp(K, N) -> int:
            # base case
            if K == 1:
                return N
            if N == 0:
                return 0
            # 避免重复计算
            if (K, N) in memo:
                return memo[(K, N)]

            res = float('INF')
            # 穷举所有可能的选择
            # for i in range(1, N + 1):
            #     res = min(res, max(dp(K, N - i), dp(K - 1, i - 1)) + 1)
            # 用二分搜索代替线性搜索
            lo, hi = 1, N
            while lo <= hi:
                mid = (lo + hi) // 2
                broken = dp(K - 1, mid - 1)  # 碎
                not_broken = dp(K, N - mid)  # 没碎
                # res = min(max(碎，没碎) + 1)
                if broken > not_broken:
                    hi = mid - 1
                    res = min(res, broken + 1)
                else:
                    lo = mid + 1
                    res = min(res, not_broken + 1)

            # 记入备忘录
            memo[(K, N)] = res
            return res

        return dp(k, n)


if __name__ == '__main__':
    print(Solution().superEggDrop(1, 2))
