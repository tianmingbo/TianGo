# -*- coding: utf-8 -*-
# @Time    : 2020/11/28 11:37
# @Author  : tmb
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        l, r = 0, len(nums) - 1
        while (l <= r):
            mid = (l + r) // 2
            if nums[mid] == target:
                return True
            if nums[l] == nums[mid]:
                l += 1
            elif nums[mid] >= nums[l]:  # 左半段有序
                if nums[l] <= target < nums[mid]:
                    r = mid - 1
                else:
                    l = mid + 1
            else:  # 右半段有序
                if nums[mid] < target <= nums[r]:
                    l = mid + 1
                else:
                    r = mid - 1
        return False


if __name__ == '__main__':
    a = Solution()
    print(a.search(nums=[1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], target=4))
