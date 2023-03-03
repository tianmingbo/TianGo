#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/3/3 17:29
    @Describe 
"""
from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        length = len(temperatures)
        ans = [0] * length
        stack = []
        for i in range(length):
            temperature = temperatures[i]
            while stack and temperature > temperatures[stack[-1]]:
                prev_index = stack.pop()
                ans[prev_index] = i - prev_index  # 索引之间的间隔
            stack.append(i)
        return ans


if __name__ == '__main__':
    a = Solution()
    print(a.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))
