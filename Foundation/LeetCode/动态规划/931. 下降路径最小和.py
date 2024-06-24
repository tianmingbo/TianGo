#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/3/3 12:57
    @Describe 
"""
from typing import List


class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        width = height = len(matrix)  # 宽高一样
        dp = [[0] * width for _ in range(width)]
        for j in range(len(matrix[0])):
            dp[0][j] = matrix[0][j]
        for i in range(1, width):
            for j in range(width):
                if j == 0:  # 对左侧边界处理
                    dp[i][j] = min(dp[i - 1][j] + matrix[i][j], dp[i - 1][j + 1] + matrix[i][j])
                elif j == width - 1:  # 处理右侧边界
                    dp[i][j] = min(dp[i - 1][j] + matrix[i][j], dp[i - 1][j - 1] + matrix[i][j])
                else:
                    dp[i][j] = min(dp[i - 1][j] + matrix[i][j], dp[i - 1][j - 1] + matrix[i][j],
                                   dp[i - 1][j + 1] + matrix[i][j])
        return min(dp[-1])


if __name__ == '__main__':
    a = Solution()
    print(a.minFallingPathSum(matrix=[[-19, 57], [-40, -5]]))
