# -*- coding: utf-8 -*-
# @Time    : 2021/1/8 19:00
# @Author  : tmb
import functools
from typing import List


class Solution:
    def singleNumbers(self, nums: List[int]) -> List[int]:
        ret = functools.reduce(lambda x, y: x ^ y, nums)
        div = 1
        while div & ret == 0:
            div <<= 1
        a, b = 0, 0
        for n in nums:
            if n & div:
                a ^= n
            else:
                b ^= n
        return [a, b]


if __name__ == '__main__':
    a = Solution()
    print(a.singleNumbers([4, 1, 4, 6]))
