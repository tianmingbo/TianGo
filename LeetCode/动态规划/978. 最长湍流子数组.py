# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 17:43
# @Author  : tmb
from typing import List


class Solution:
    def maxTurbulenceSize(self, arr: List[int]) -> int:
        if len(set(arr)) == 1:
            return 1
        res = -float('inf')
        dp = [0 for _ in range(len(arr))]
        #  [0, -5, -2, 8, -3, 1, 0, -7, 8]  -2, 8, -3, 1 符号不同
        differ = [0] + [arr[i] - arr[i - 1] for i in range(1, len(arr))]
        for i in range(1, len(differ)):
            if differ[i] * differ[i - 1] < 0:
                dp[i] = dp[i - 1] + 1
            else:
                dp[i] = 1
            res = dp[i] if dp[i] > res else res
        return res + 1


if __name__ == '__main__':
    a = Solution()
    print(a.maxTurbulenceSize([9, 4, 2, 10, 7, 8, 8, 1, 9]))
