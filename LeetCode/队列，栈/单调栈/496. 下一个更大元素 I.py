#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/3/5 12:45
    @Describe 
"""
from typing import List


class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        res = {}
        stack = []
        for num in reversed(nums2):
            """
            while 循环是把两个 大值 元素之间的元素排除，因为他们的存在没有意义，
            前面挡着个「更大」的元素，所以他们不可能被作为后续进来的元素的下一个更大元素了。
            """
            while stack and num >= stack[-1]:
                stack.pop()
            res[num] = stack[-1] if stack else -1
            stack.append(num)
        return [res[num] for num in nums1]


if __name__ == '__main__':
    print(Solution().nextGreaterElement(nums1=[4, 1, 2], nums2=[1, 3, 4, 2]))
