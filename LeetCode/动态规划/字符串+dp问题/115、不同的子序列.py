# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 22:03
# @Author  : tmb
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        row, col = len(t), len(s)
        dp = [[0 for _ in range(col + 1)] for _ in range(row + 1)]
        for i in range(col + 1):
            dp[0][i] = 1
        for i in range(1, row + 1):  # 遍历行
            for j in range(1, col + 1):  # 遍历列
                if t[i - 1] == s[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + dp[i][j - 1]
                else:
                    dp[i][j] = dp[i][j - 1]
        print(dp)
        return dp[row][col]
'''
状态转移方程：
if s[i]==s[j] : dp[i][j]= dp[i-1][j-1] + dp[i][j-1]
else : dp[i][j] = dp[i][j-1]
'''

if __name__ == '__main__':
    a = Solution()
    print(a.numDistinct('rabbbit', 'rabbit'))
