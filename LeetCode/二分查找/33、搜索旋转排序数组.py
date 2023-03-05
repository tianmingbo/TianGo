# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 15:44
# @Author  : tmb
class Solution:
    def search(self, nums, target: int) -> int:
        n = len(nums)
        left, right = 0, n - 1
        while (left <= right):
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[0] <= nums[mid]:  # 如果0-mid是有序的
                if nums[0] <= target < nums[mid]:  # 如果target在0~mid之间
                    right = mid - 1
                else:
                    left = mid + 1
            else:  # 0-mid无序，则mid~n是有序的
                if nums[mid] < target <= nums[n - 1]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1


if __name__ == '__main__':
    a = Solution()
    print(a.search([4, 5, 6, 7, 0, 1, 2], 0))
