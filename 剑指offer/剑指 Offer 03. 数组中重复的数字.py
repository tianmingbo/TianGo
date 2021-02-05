# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 20:26
# @Author  : tmb
from typing import List

'''
使用hash表，快速解决
'''


class Solution:
    def findRepeatNumber(self, nums: List[int]) -> int:
        hash = set()
        for i in nums:
            if i not in hash:
                hash.add(i)
            else:
                return i


if __name__ == '__main__':
    a = Solution()
    print(a.findRepeatNumber([0, 1, 2, 3, 4, 11, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))
