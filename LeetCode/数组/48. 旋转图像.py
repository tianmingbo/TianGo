# -*- coding: utf-8 -*-
# @Time    : 2020/12/7 20:03
# @Author  : tmb
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        for i in range(n):
            for j in range(i, n):
                matrix[j][i], matrix[i][j] = matrix[i][j], matrix[j][i]
        for k in range(n):
            matrix[k].reverse()


if __name__ == '__main__':
    a = Solution()
    print(a.rotate(matrix=
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]))
