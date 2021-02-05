# -*- coding: utf-8 -*-
# @Time    : 2020/12/26 20:58
# @Author  : tmb
from typing import List


class Solution:
    def findNumberIn2DArray(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix:
            return False
        raw, col = 0, len(matrix[0]) - 1
        while raw <= len(matrix) - 1 and col >= 0:
            if matrix[raw][col] > target:
                col -= 1
            elif matrix[raw][col] < target:
                raw += 1
            else:
                return True
        return False


if __name__ == '__main__':
    a = Solution()
    print(a.findNumberIn2DArray([
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30]
    ], 20))
