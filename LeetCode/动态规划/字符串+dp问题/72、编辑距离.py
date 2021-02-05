# -*- coding: utf-8 -*-
# @Time    : 2020/10/27 12:40
# @Author  : tmb
'''
类似转换问题，变成二维矩阵格式
'''


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        if len(word1) == 0:
            return len(word2)
        if len(word2) == 0:
            return len(word1)
        first, second = len(word1), len(word2)
        dp = [[0 for _ in range(second + 1)] for _ in range(first + 1)]
        for i in range(first + 1):
            dp[i][0] = i
        for j in range(second + 1):
            dp[0][j] = j

        for x in range(1, first + 1):
            for y in range(1, second + 1):
                if word1[x - 1] == word2[y - 1]:
                    dp[x][y] = dp[x - 1][y - 1]
                else:
                    dp[x][y] = min(dp[x - 1][y] + 1, dp[x][y - 1] + 1, dp[x - 1][y - 1] + 1)
        return dp[first][second]


if __name__ == '__main__':
    a = Solution()
    print(a.minDistance('horse', 'ros'))
