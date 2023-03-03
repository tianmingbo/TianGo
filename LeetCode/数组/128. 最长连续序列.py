#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/3/3 17:22
    @Describe 
"""

from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        res = 0
        my_set = set(nums)
        # O(n)
        for num in nums:
            left, right = 0, 0
            while num - left - 1 in my_set:  # 向左探
                my_set.discard(num - left - 1)
                left += 1
            while num + right + 1 in my_set:  # 向右探 in O(1)
                my_set.discard(num + right + 1)
                right += 1
            res = max(res, left + right + 1)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.longestConsecutive(nums=[100, 4, 200, 1, 3, 2]))
