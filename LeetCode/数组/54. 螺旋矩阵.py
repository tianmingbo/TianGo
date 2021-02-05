# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 18:47
# @Author  : tmb
from typing import List

'''
思路：追层遍历
left，right，top，bottom
'''


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix:
            return []
        if len(matrix) == 1:
            return matrix[0]
        counter = len(matrix) * len(matrix[0])
        left, right, top, bottom = 0, len(matrix[0]) - 1, 0, len(matrix) - 1
        res = []
        while counter >= 1:
            # 从左到右
            for i in range(left, right + 1):
                if counter >= 1:
                    res.append(matrix[top][i])
                    counter -= 1
            top += 1

            # 从上到下
            for j in range(top, bottom + 1):
                if counter >= 1:
                    res.append(matrix[j][right])
                    counter -= 1
            right -= 1

            # 从右到左
            for k in range(right, left - 1, -1):
                if counter >= 1:
                    res.append(matrix[bottom][k])
                    counter -= 1
            bottom -= 1

            # 从下到上
            for z in range(bottom, top - 1, -1):
                if counter >= 1:
                    res.append(matrix[z][left])
                    counter -= 1
            left += 1

        return res


if __name__ == '__main__':
    a = Solution()
    print(a.spiralOrder([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]))
