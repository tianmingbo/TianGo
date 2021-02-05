# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 21:15
# @Author  : tmb
# -*- coding:utf-8 -*-

class Solution:
    '''
    快排排序，返回第n-K个
    '''

    def findKth(self, a, n, K):
        self.quick_sort(a, 0, n - 1, K)
        return a[n - K]

    def quick_sort(self, arr, begin, end, K):
        if begin >= end:
            return
        pivot_index = self.partition(arr, begin, end)
        while pivot_index != len(arr) - K:
            if pivot_index < len(arr) - K:
                self.quick_sort(arr, begin, pivot_index - 1, K)
            else:
                self.quick_sort(arr, pivot_index + 1, end, K)

    def partition(self, arr, begin, end):
        prepare = arr[begin]
        mark = begin
        for i in range(begin + 1, end + 1):
            if arr[i] < prepare:
                mark += 1
                arr[mark], arr[i] = arr[i], arr[mark]
        arr[mark], arr[begin] = arr[begin], arr[mark]
        return mark


'''
未理解2
'''

from typing import List

'''
利用快排思想，部分排序
'''


class Solution2:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        n = len(nums)
        start, end = 0, n - 1
        pivot = -1
        while pivot != n - k:
            print(nums)
            if pivot < n - k:
                # 说明倒数第K个在pivot右边，在右边查找
                start, pivot, t = self.partition(nums, pivot + 1, end)
            else:  # 在pivot左边
                start, pivot, t = self.partition(nums, start, pivot - 1)
        return nums[pivot]

    def partition(self, nums, start, end):
        '''
        双指针，找到pilot应该在的位置
        '''
        pilot = start
        l = start + 1
        r = end
        while l <= r:
            if nums[l] > nums[pilot]:
                nums[l], nums[r] = nums[r], nums[l]
                r -= 1
            else:
                l += 1
        nums[pilot], nums[r] = nums[r], nums[pilot]  # pilot的位置已经确定，右边是比pilot大的元素，左边是小的元素
        return start, r, end


if __name__ == '__main__':
    a = Solution()
    print(a.findKth(
        [1332802, 1177178, 1514891, 871248, 753214, 123866, 1615405, 328656, 1540395, 968891, 1884022, 252932, 1034406,
         1455178, 821713, 486232, 860175, 1896237, 852300, 566715, 1285209, 1845742, 883142, 259266, 520911, 1844960,
         218188, 1528217, 332380, 261485, 1111670, 16920, 1249664, 1199799, 1959818, 1546744, 1904944, 51047, 1176397,
         190970, 48715, 349690, 673887, 1648782, 1010556, 1165786, 937247, 986578, 798663], 49, 24))
