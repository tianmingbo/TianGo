# -*- coding: utf-8 -*-
# @Time    : 2021/1/20 21:57
# @Author  : tmb
import math


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need, window = {}, {}
        for i in t:
            if i in need:
                need[i] += 1
            else:
                need[i] = 1
        left, right, valid = 0, 0, 0
        start, length = 0, math.inf
        while right < len(s):
            # c 是将移入窗口的字符
            c = s[right]
            # 右移窗口
            right += 1
            # 进行窗口内数据的一系列更新
            if c in need:
                if c in window:
                    window[c] += 1
                else:
                    window[c] = 1
                if window[c] == need[c]:
                    valid += 1
            # 判断左侧窗口是不是收缩
            while valid == len(need):
                # 收缩窗口
                if right - left < length:
                    start = left
                    length = right - left
                # 移出窗口
                d = s[left]
                # 左移窗口
                left += 1
                # 窗口内数据更新
                if d in need:
                    if window[d] == need[d]:
                        valid -= 1
                    window[d] -= 1
        return "" if length == math.inf else s[start: start + length]
