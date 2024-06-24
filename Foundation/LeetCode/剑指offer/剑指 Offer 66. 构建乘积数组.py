# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 20:12
# @Author  : tmb
from typing import List


class Solution:
    def constructArr(self, a: List[int]) -> List[int]:
        forward = [1 for _ in a]
        back = [1 for _ in a]
        for i in range(1, len(a)):  # [1,2,4,12,48] 从后往前
            back[i] = back[i - 1] * a[i - 1]
        for j in range(len(a) - 2, -1, -1):  # [120,60,20,5,1] #从前往后
            forward[j] = forward[j + 1] * a[j + 1]
        return [forward[i] * back[i] for i in range(len(a))]


if __name__ == '__main__':
    a = Solution()
    print(a.constructArr([2, 2, 3, 4, 5]))
