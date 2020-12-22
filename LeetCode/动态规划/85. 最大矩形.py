# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 15:28
# @Author  : tmb
from typing import List


class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix:
            return 0
        raw, col = len(matrix), len(matrix[0])
        dp = [[0] * col for _ in range(raw)]
        for i in range(raw):
            for j in range(col):
                if matrix[i][j] == '0':
                    dp[i][j] = 0
                else:
                    if i - 1 < 0:
                        if matrix[i][j] == '1':
                            dp[i][j] = 1
                    if j - 1 < 0:
                        if matrix[i][j] == '1' and dp:
                            dp[i][j] = 1
        print(dp)


class Solution2:
    # 未理解
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        maxarea = 0
        dp = [[0] * len(matrix[0]) for _ in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == '0': continue

                # compute the maximum width and update dp with it
                width = dp[i][j] = dp[i][j - 1] + 1 if j else 1

                # compute the maximum area rectangle with a lower right corner at [i, j]
                for k in range(i, -1, -1):
                    width = min(width, dp[k][j])
                    maxarea = max(maxarea, width * (i - k + 1))
        return maxarea


if __name__ == '__main__':
    a = Solution2()
    print(a.maximalRectangle(matrix=[["1", "0", "1", "0", "0"],
                                     ["1", "0", "1", "1", "1"],
                                     ["1", "1", "1", "1", "1"],
                                     ["1", "0", "0", "1", "0"]]))
