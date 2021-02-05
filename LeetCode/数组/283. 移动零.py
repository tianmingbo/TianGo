# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 21:26
# @Author  : tmb
class Solution:
    def moveZeroes(self, nums) -> None:
        if not nums:
            return
        j = 0
        for k in range(len(nums)):
            if nums[k]:
                nums[j], nums[k] = nums[k], nums[j]
                j += 1
        print(nums)


if __name__ == '__main__':
    a = Solution()
    a.moveZeroes([0, 1, 0, 3, 12])

'''
双指针，i记录当前位置，j记录0的个数
'''
