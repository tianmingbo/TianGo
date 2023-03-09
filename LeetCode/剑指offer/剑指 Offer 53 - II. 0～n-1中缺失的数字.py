# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 18:57
# @Author  : tmb
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (right + left) // 2
            if nums[mid] == mid:
                left = mid + 1
            elif nums[mid] > mid:
                right = mid - 1
        if mid == nums[mid]:  # [0,1,2,3] 这种情况
            mid += 1
        return mid


if __name__ == '__main__':
    a = Solution()
    print(a.missingNumber([0]))
