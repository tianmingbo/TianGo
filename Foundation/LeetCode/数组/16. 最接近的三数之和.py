# -*- coding: utf-8 -*-
# @Time    : 2020/11/28 12:13
# @Author  : tmb
from typing import List


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        tmp, res = float('inf'), 0
        for k in range(len(nums) - 1):
            i = k + 1
            j = len(nums) - 1
            while i < j:
                a = abs((nums[k] + nums[i] + nums[j]) - target)
                if a < tmp:
                    tmp = a
                    res = nums[k] + nums[i] + nums[j]
                if nums[k] + nums[i] + nums[j] == target:
                    return nums[k] + nums[i] + nums[j]
                if nums[k] + nums[i] + nums[j] > target:
                    j -= 1
                elif nums[k] + nums[i] + nums[j] < target:
                    i += 1
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.threeSumClosest(nums=[-1, 2, 1, -4], target=1))
