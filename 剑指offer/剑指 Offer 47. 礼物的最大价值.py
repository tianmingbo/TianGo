from typing import List


class Solution:
    def maxValue(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0
        dp = [[0] * len(grid[0]) for _ in range(len(grid))]
        dp[0][0] = grid[0][0]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if i - 1 == -1 and j - 1 >= 0:
                    dp[0][j] = dp[0][j - 1] + grid[0][j]
                elif j - 1 == -1 and i - 1 >= 0:
                    dp[i][0] = dp[i - 1][0] + grid[i][0]
                elif i - 1 >= 0 and j - 1 >= 0:
                    dp[i][j] = max(grid[i][j] + dp[i - 1][j], grid[i][j] + dp[i][j - 1])
        return dp[-1][-1]


if __name__ == '__main__':
    a = Solution()
    print(a.maxValue([
        [1, 2, 2],
    ]))
