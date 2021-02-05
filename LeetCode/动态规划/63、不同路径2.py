# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 11:57
# @Author  : tmb
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid) -> int:
        raw = len(obstacleGrid)
        col = len(obstacleGrid[0])
        dp = [[0 for _ in range(col)] for _ in range(raw)]
        for i in range(raw):
            for j in range(col):
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = -1
        if dp[raw - 1][col - 1] == -1 or dp[0][0] == -1:
            return 0
        dp[raw - 1][col - 1] = 1
        for i in range(raw - 2, -1, -1):  # 处理最后一列
            if dp[i][col - 1] == -1:
                continue
            else:
                dp[i][col - 1] = dp[i + 1][col - 1]
        for j in range(col - 2, -1, -1):  # 处理最后一行
            if dp[raw - 1][j] == -1:
                continue
            else:
                dp[raw - 1][j] = dp[raw - 1][j + 1]
        for x in range(raw - 2, -1, -1):  # 主逻辑，从下往上，当前元素有两种可能（下边的和右边的），都加上
            for y in range(col - 2, -1, -1):
                if dp[x][y] == -1:
                    continue
                if dp[x + 1][y] == -1 and dp[x][y + 1] == -1:
                    dp[x][y] = 0
                elif dp[x][y + 1] == -1:
                    dp[x][y] = dp[x + 1][y]
                elif dp[x + 1][y] == -1:
                    dp[x][y] = dp[x][y + 1]
                else:
                    dp[x][y] = dp[x + 1][y] + dp[x][y + 1]
        return dp[0][0]


class Solution2:
    def uniquePathsWithObstacles(self, obstacleGrid):
        dp = [[0] * len(obstacleGrid[0]) for _ in range(len(obstacleGrid))]
        dp[0][0] = 1 if obstacleGrid[0][0] == 0 else 0
        for i in range(len(obstacleGrid)):
            for j in range(len(obstacleGrid[0])):
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = 0
                else:
                    if i - 1 >= 0:  # 排除第一行，上面为空
                        dp[i][j] += dp[i - 1][j]
                    if j - 1 >= 0:  # 排除第一列，左面为空
                        dp[i][j] += dp[i][j - 1]
        return dp[-1][-1]


if __name__ == '__main__':
    a = Solution2()
    a.uniquePathsWithObstacles([[0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 0, 0]])
    # print(a.uniquePathsWithObstacles([[1, 0]]))
