# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 9:34
# @Author  : tmb
from typing import List


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        if not nums:
            return 0
        left, right = 0, len(nums) - 1
        while left < right:  # 不能<=
            mid = (left + right) >> 1
            if nums[mid] > nums[mid + 1]:
                right = mid
            elif nums[mid] < nums[mid + 1]:
                left = mid + 1
        return left


'''
为什么二分查找大的那一半一定会有峰值呢？（即nums[mid]<nums[mid+1]时，mid+1~N一定存在峰值），首先已知 nums[mid+1]>nums[mid]，
那么mid+2只有两种可能，一个是大于mid+1，一个是小于mid+1，小于mid+1的情况，那么mid+1就是峰值，大于mid+1的情况，继续向右推，如果一直到数组的末尾都是大于的，那么可以肯定最后一个元素是峰值，
因为nums[nums.length]=负无穷
'''
if __name__ == '__main__':
    a = Solution()
    print(a.findPeakElement([1, 2, 1, 3, 5, 6, 4]))
