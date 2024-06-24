# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 19:47
# @Author  : tmb
from typing import List

'''
摩尔投票法：
众数个数大于总数的一半，每次是众数，票数加1，不是众数，票数减1，
最终得出的数，一定是众数
'''


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        votes = 0
        res = nums[0]
        for i in nums:
            if votes == 0:
                res = i
            votes = votes + 1 if res == i else votes - 1
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.majorityElement([5, 5, 6]))
