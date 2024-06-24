# -*- coding: utf-8 -*-
# @Time    : 2021/1/8 19:15
# @Author  : tmb
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        l, r = 0, len(nums) - 1
        res = []
        while l < r:

            if nums[l] + nums[r] == target:
                res.append(nums[l])
                res.append(nums[r])
                l += 1
                r -= 1
                break
            if nums[l] + nums[r] < target:
                l += 1
            elif nums[l] + nums[r] > target:
                r -= 1
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.twoSum([16, 16, 18, 24, 30, 32], 48))
