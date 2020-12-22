# -*- coding: utf-8 -*-
# @Time    : 2020/12/17 19:24
# @Author  : tmb
from typing import List


class Solution:
    def transpose(self, A: List[List[int]]) -> List[List[int]]:
        res = [[0] * len(A) for _ in range(len(A[0]))]
        for i in range(len(A)):
            for j in range(len(A[0])):
                res[j][i] = A[i][j]
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.transpose([[1, 2, 3], [4, 5, 6]]))
