#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/2/28 18:58
    @Describe 
"""
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        res = []
        need, window = {}, {}
        for i in p:
            if i in need:
                need[i] += 1
            else:
                need[i] = 1
        left, right, valid = 0, 0, 0
        while right < len(s):
            c = s[right]
            right += 1
            if c in need:
                if c in window:
                    window[c] += 1
                else:
                    window[c] = 1
                if window[c] == need[c]:
                    valid += 1
            while valid == len(need):
                if right - left == len(p):  # 限制等于子串长度
                    res.append(left)
                d = s[left]
                left += 1
                if d in need:
                    if window[d] == need[d]:
                        valid -= 1
                    window[d] -= 1
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.findAnagrams(s="cbaebabacd", p="abc"))
