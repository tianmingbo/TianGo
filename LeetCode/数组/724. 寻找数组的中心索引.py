# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 22:02
# @Author  : tmb
from typing import List


class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        n = len(nums)
        sums = sum(nums)
        preSum = 0
        for i in range(n):
            if preSum == sums - preSum - nums[i]:
                return i
            preSum += nums[i]
        return -1


if __name__ == '__main__':
    a = Solution()
    print(a.pivotIndex([1, 7, 3, 6, 5, 6]))
