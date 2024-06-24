# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 15:24
# @Author  : tmb
'''
动态规划
'''


class Solution:
    def minPathSum(self, grid):
        if not grid:
            return 0
        width = len(grid[0]) - 1
        height = len(grid) - 1
        dp = [[0 for i in j] for j in grid]
        dp[height][width] = grid[height][width]

        for y in range(height - 1, -1, -1):  # 对最后一列进行处理
            dp[y][width] = grid[y][width] + dp[y + 1][width]

        for x in range(width - 1, -1, -1):  # 对最后一行进行处理
            dp[height][x] = grid[height][x] + dp[height][x + 1]

        # 只能往下或往右走，从下往上时，判断右方的和下方的哪个值小
        for i in range(len(grid) - 2, -1, -1):
            for j in range(len(grid[i]) - 2, -1, -1):
                dp[i][j] = min(grid[i][j] + dp[i + 1][j], grid[i][j] + dp[i][j + 1])
        return dp[0][0]  # 从下往上走，左上角的就是最小路径和

    def minPathSum2(self, grid):
        if not grid:
            return 0
        dp = [[0] * (len(grid[0]) + 1) for _ in range(len(grid) + 1)]
        dp[1][1] = grid[0][0]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if i == 0:
                    dp[i + 1][j + 1] = grid[i][j] + dp[i + 1][j]
                if j == 0:
                    dp[i + 1][j + 1] = grid[i][j] + dp[i][j + 1]
                elif i > 0 and j > 0:
                    dp[i + 1][j + 1] = min(dp[i + 1][j] + grid[i][j], dp[i][j + 1] + grid[i][j])
        return dp[-1][-1]


if __name__ == '__main__':
    a = Solution()
    print(a.minPathSum2([[1, 3, 1],
                         [1, 5, 1]]))
