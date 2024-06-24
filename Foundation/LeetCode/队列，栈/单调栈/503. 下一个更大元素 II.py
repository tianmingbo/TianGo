#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/3/5 12:47
    @Describe 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/3/5 12:45
    @Describe 
"""
from typing import List


class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        stack = []
        tmp = nums + nums  # 双倍扩展
        res = []
        for i in range(len(tmp) - 1, -1, -1):
            while stack and tmp[i] >= stack[-1]:
                stack.pop()
            res.append(stack[-1] if stack else -1)
            stack.append(tmp[i])
        return res[::-1][:n]


if __name__ == '__main__':
    print(Solution().nextGreaterElements(nums=[1, 2, 1]))
