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

    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix: return 0

        m = len(matrix)
        n = len(matrix[0])

        left = [0] * n  # initialize left as the leftmost boundary possible
        right = [n] * n  # initialize right as the rightmost boundary possible
        height = [0] * n

        maxarea = 0

        for i in range(m):

            cur_left, cur_right = 0, n
            # update height
            for j in range(n):
                if matrix[i][j] == '1':
                    height[j] += 1
                else:
                    height[j] = 0
            # update left
            for j in range(n):
                if matrix[i][j] == '1':
                    left[j] = max(left[j], cur_left)
                else:
                    left[j] = 0
                    cur_left = j + 1
            # update right
            for j in range(n - 1, -1, -1):
                if matrix[i][j] == '1':
                    right[j] = min(right[j], cur_right)
                else:
                    right[j] = n
                    cur_right = j
            # update the area
            for j in range(n):
                maxarea = max(maxarea, height[j] * (right[j] - left[j]))

        return maxarea


if __name__ == '__main__':
    a = Solution2()
    print(a.maximalRectangle(matrix=[["1", "0", "1", "0", "0"],
                                     ["1", "0", "1", "1", "1"],
                                     ["1", "1", "1", "1", "1"],
                                     ["1", "0", "0", "1", "0"]]))
