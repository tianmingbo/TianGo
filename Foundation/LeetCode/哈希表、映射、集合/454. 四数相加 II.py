# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 18:45
# @Author  : tmb
from typing import List


class Solution:
    def fourSumCount(self, A: List[int], B: List[int], C: List[int], D: List[int]) -> int:
        hash_ab = {}
        count = 0
        for i in A:
            for j in B:
                if i + j not in hash_ab:
                    hash_ab[i + j] = 1
                else:
                    hash_ab[i + j] += 1
        for x in C:
            for y in D:
                if 0 - (x + y) in hash_ab:  # 0= hash_ab中的元素+（x+y）
                    count += hash_ab[0 - (x + y)]
        return count


if __name__ == '__main__':
    a = Solution()
    print(a.fourSumCount([-1, -1],
                         [-1, 1],
                         [-1, 1],
                         [1, -1]))
