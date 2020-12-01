# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 20:06
# @Author  : tmb
from typing import List


class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if len(nums) == 1:
            return
        r = len(nums) - 2
        while r >= 0:
            if nums[-1] > nums[r]:
                break
            else:
                r -= 1
        if r < 0:
            nums.sort()
        else:
            # while nums[r] == nums[r - 1]:
            #     r -= 1
            if r == 0:
                nums.insert(0, nums[-1])
                nums.pop()
            else:
                nums[-1], nums[r] = nums[r], nums[-1]
        print(nums)


if __name__ == '__main__':
    a = Solution()
    a.nextPermutation([3, 2,1,4,5])
