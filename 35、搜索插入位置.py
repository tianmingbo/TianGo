# -*- coding: utf-8 -*-
# @Time    : 2020/8/25 16:03
# @Author  : tmb

'''示例 1:
二分法
输入: [1,3,5,6], 5
输出: 2

示例 2:

输入: [1,3,5,6], 2
输出: 1
'''

#O(n)
class Solution:
    def searchInsert(self, nums, target):
        if not nums:
            return -1
        for i, num in enumerate(nums):
            if num >= target:
                return i
        return len(nums)

#O(logn)
class Soluction2:
    def searchInsert(self, nums, target):
        minimum = 0
        maximum = len(nums)
        mid = (maximum + minimum) // 2
        while minimum < maximum:
            if nums[mid] > target:
                maximum = mid
            elif nums[mid] < target:
                minimum = mid + 1
            else:
                return mid
            mid = (maximum + minimum) // 2

        return mid


if __name__ == '__main__':
    a = Soluction2()
    print(a.searchInsert([1, 3, 3, 4, 5, 6], 7))
