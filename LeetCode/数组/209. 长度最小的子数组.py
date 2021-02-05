# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 20:31
# @Author  : tmb
from typing import List


class Solution:
    def minSubArrayLen(self, s: int, nums: List[int]) -> int:
        if not nums:
            return 0
        '''
        双指针，只要加上当前end的值大于s，更新长度，然后减去start的值
        '''
        n = len(nums)
        res = n + 1
        start, end = 0, 0
        tmp = 0
        while end < n:
            tmp += nums[end]
            while tmp >= s:
                res = min(end - start + 1, res)
                tmp -= nums[start]
                start += 1
            end += 1
        return 0 if res == n + 1 else res


if __name__ == '__main__':
    a = Solution()
    print(a.minSubArrayLen(s=7, nums=[2, 3, 1, 2, 4, 7]))
