# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 20:22
# @Author  : tmb
from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        '''
        单指针，先排0，再排1
        '''
        p = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                nums[i], nums[p] = nums[p], nums[i]
                p += 1
        for j in range(p, len(nums)):
            if nums[j] == 1:
                nums[j], nums[p] = nums[p], nums[j]
                p += 1


if __name__ == '__main__':
    a = Solution()
    print(a.sortColors(
        nums=[2, 0, 1, 1, 1, 1, 1, 1, 1]))
