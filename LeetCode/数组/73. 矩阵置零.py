# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 15:53
# @Author  : tmb
from typing import List

'''
my
'''


class Solution:

    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        self.flag = [[False] * len(matrix[0]) for _ in range(len(matrix))]
        raw, col = len(matrix), len(matrix[0])
        for i in range(raw):
            for j in range(col):
                if matrix[i][j] == 0 and not self.flag[i][j]:
                    self.deal_matrix(matrix, i, j)
        # print(matrix)

    def deal_matrix(self, matrix, raw, col):
        """
        :param raw:行
        :param col: 列
        :return:
        """
        for i in range(len(matrix[0])):
            if matrix[raw][i - 1] != 0:
                matrix[raw][i - 1] = 0
                self.flag[raw][i - 1] = True
        for j in range(len(matrix)):
            if matrix[j - 1][col] != 0:
                matrix[j - 1][col] = 0
                self.flag[j - 1][col] = True


if __name__ == '__main__':
    a = Solution()
    a.setZeroes([
        [0, 1, 2, 0],
        [3, 4, 5, 2],
        [1, 3, 1, 5]
    ])
