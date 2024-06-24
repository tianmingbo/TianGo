# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 14:15
# @Author  : tmb
'''
双指针
'''
class Solution:
    def removeElement(self, nums, val):
        if not nums:
            return
        i = 0
        for j in range(len(nums)):
            if nums[j] != val:
                nums[i] = nums[j]
                i += 1
        # nums = nums[:i]
        return i


if __name__ == '__main__':
    a = Solution()
    print(a.removeElement([0, 1, 2, 2, 3, 0, 4, 2], 2))
