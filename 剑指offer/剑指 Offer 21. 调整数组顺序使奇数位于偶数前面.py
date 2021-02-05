# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 18:30
# @Author  : tmb
from typing import List


class Solution:
    def exchange(self, nums: List[int]) -> List[int]:
        '''
        双指针，奇数向前移动，偶数向后移动
        :param nums:
        :return:
        '''
        l, r = 0, len(nums) - 1
        while l < r:
            if nums[l] % 2 != 0:
                l += 1
            elif nums[l] % 2 == 0 and nums[r] % 2 == 1:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1
            else:
                r -= 1
        return nums


if __name__ == '__main__':
    a = Solution()
    print(a.exchange([1, 2, 3, 3, 3, 3, 3, 3, 4]))
