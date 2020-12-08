# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 14:28
# @Author  : tmb
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        num_set = set(nums)
        n = len(nums) + 1
        for number in range(n):
            if number not in num_set:
                return number


if __name__ == '__main__':
    a = Solution()
    print(a.missingNumber(nums=[3, 0, 1]))
