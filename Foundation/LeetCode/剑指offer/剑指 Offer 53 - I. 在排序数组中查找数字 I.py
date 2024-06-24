# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 21:06
# @Author  : tmb
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        hash_table = {}
        for i in nums:
            if i not in hash_table:
                hash_table[i] = 1
            else:
                hash_table[i] += 1
        if target not in hash_table:
            return 0
        return hash_table[target]


class Solution2:
    def search(self, nums: [int], target: int) -> int:
        # 搜索右边界 right
        i, j = 0, len(nums) - 1
        while i <= j:
            m = (i + j) // 2
            if nums[m] <= target:
                i = m + 1
            else:
                j = m - 1
        right = i
        # 若数组中无 target ，则提前返回
        if j >= 0 and nums[j] != target:
            return 0
        # 搜索左边界 left
        i = 0
        while i <= j:
            m = (i + j) // 2
            if nums[m] < target:
                i = m + 1
            else:
                j = m - 1
        left = j
        return right - left - 1


if __name__ == '__main__':
    a = Solution2()
    print(a.search(nums=[2, 2], target=3))
