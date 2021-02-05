# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 10:11
# @Author  : tmb
from typing import List


# 计数排序
class Solution:
    def relativeSortArray(self, arr1: List[int], arr2: List[int]) -> List[int]:
        max_num = max(arr1)
        space = [0 for _ in range(max_num + 1)]
        for i in arr1:
            space[i] += 1

        res = []
        for j in arr2:
            res.extend([j] * space[j])
            space[j] = 0

        for k in range(len(space)):
            if space[k] != 0:
                res.extend([k] * space[k])
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.relativeSortArray(arr1=[2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], arr2=[2, 1, 4, 3, 9, 6]))
