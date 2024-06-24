# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 21:17
# @Author  : tmb
from typing import List


class Solution:
    def minArray(self, numbers: List[int]) -> int:
        left, right = 0, len(numbers) - 1
        while left <= right:
            mid = (right - left) // 2

