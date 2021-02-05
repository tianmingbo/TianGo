# -*- coding: utf-8 -*-
# @Time    : 2020/11/26 11:41
# @Author  : tmb
from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        a = self.find_left_bound(nums, target)
        b = self.find_right_bound(nums, target)
        return [a, b]

    def find_left_bound(self, nums, target):
        # 二分模板
        if not nums:
            return -1
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (right + left) >> 1
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            elif nums[mid] == target:  # 等于后不退出，继续在左边找
                right = mid - 1
        if left >= len(nums) or nums[left] != target:  # 如果target大于所有值，那么left会等于len(nums)
            return -1
        return left

    def find_right_bound(self, nums, target):
        if not nums:
            return -1
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (right + left) >> 1
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            elif nums[mid] == target:  # 等于后不退出，继续在右边找
                left = mid + 1
        if right < 0 or nums[right] != target:  # 如果target小于所有值，right等于-1
            return -1
        return right


if __name__ == '__main__':
    a = Solution()
    print(a.searchRange(nums=[5, 7, 7, 8, 8, 10], target=8))
