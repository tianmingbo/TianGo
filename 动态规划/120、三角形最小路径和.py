# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 14:01
# @Author  : tmb

class Solution:
    def minimumTotal(self, triangle):
        if not triangle:
            return 0
        max_len = len(max(triangle, key=len))
        dp = [[None for i in range(max_len)] for j in range(max_len)]
        for index, elem in enumerate(triangle):
            if index == 0:
                dp[0][0] = triangle[index][0]
            else:
                for j in range(len(elem)):
                    if j == 0:  # 最左边的值，另外处理
                        dp[index][j] = triangle[index][j] + dp[index - 1][j]
                    elif dp[index - 1][j] != None and dp[index - 1][j - 1] != None:  # 向上保证头上的和左上角的值存在
                        dp[index][j] = min(triangle[index][j] + dp[index - 1][j - 1],
                                           triangle[index][j] + dp[index - 1][j])
                    else:
                        dp[index][j] = triangle[index][j] + dp[index - 1][j - 1]  # 头上没有值，左上角有值
        return min(dp[-1])


if __name__ == '__main__':
    a = Solution()
    print(a.minimumTotal([[2],
                          [-6, 7],
                          [4, -8, 7],
                          [4, -6, 7, -1],
                          [4, 8, -8, 0, -4],
                          [-3, -4, -5, 3, 2, 2]]))
