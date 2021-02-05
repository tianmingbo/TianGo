# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 14:25
# @Author  : tmb
class Solution:
    def longestCommonSubsequence(self, text1, text2) -> int:
        if not text1 or not text2:
            return 0
        m, n = len(text1), len(text2)
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]  # 存储状态
        for i in range(1, m + 1):  # 遍历每行
            for j in range(1, n + 1):  # 遍历每列
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        print(dp)
        return dp[m][n]


if __name__ == '__main__':
    s = Solution()
    print(s.longestCommonSubsequence('abcde', 'ace'))
