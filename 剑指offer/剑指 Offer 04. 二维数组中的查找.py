# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 20:33
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
