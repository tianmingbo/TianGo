# -*- coding: utf-8 -*-
# @Time    : 2021/2/1 20:32
# @Author  : tmb
from typing import List

'''
和最长公共子序列区分开来
'''


class Solution:
    def findLength(self, A: List[int], B: List[int]) -> int:
        m, n = len(A), len(B)
        max_len, end = 0, 0
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        for i in range(1, m + 1):  # 遍历每行
            for j in range(1, n + 1):  # 遍历每列
                if A[i - 1] == B[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = 0
                max_len = max(max_len, dp[i][j])  # 记录最长
        return max_len


class Solution2:
    def LCS(self, str1, str2):
        # write code here
        if len(str1) > len(str2):
            str1, str2 = str2, str1
        max_len, res = 0, ''
        for i in range(len(str1)):
            if str1[i - max_len: i + 1] in str2:
                res = str1[i - max_len: i + 1]
                max_len += 1
        return '-1' if not res else res


if __name__ == '__main__':
    a = Solution()
    print(a.findLength([1, 2, 3, 2, 1], [3, 2, 1, 4, 7]))
