# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 19:38
# @Author  : tmb
from typing import List


class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        if not n:
            return []
        matrix = [[0] * n for _ in range(n)]
        counter = 1
        left, right, top, bottom = 0, n - 1, 0, n - 1
        while counter <= n ** 2:
            # 从左到右
            for i in range(left, right + 1):
                if counter <= n ** 2:
                    matrix[top][i] = counter
                    counter += 1
            top += 1

            # 从上到下
            for j in range(top, bottom + 1):
                if counter <= n ** 2:
                    matrix[j][right] = counter
                    counter += 1
            right -= 1

            # 从右到左
            for k in range(right, left - 1, -1):
                if counter <= n ** 2:
                    matrix[bottom][k] = counter
                    counter += 1
            bottom -= 1

            # 从下到上
            for z in range(bottom, top - 1, -1):
                if counter <= n ** 2:
                    matrix[z][left] = counter
                    counter += 1
            left += 1

        return matrix


if __name__ == '__main__':
    a = Solution()
    print(a.generateMatrix(3))
