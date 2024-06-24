# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 19:06
# @Author  : tmb
from typing import List


class Solution:
    def isStraight(self, nums: List[int]) -> bool:
        j = 0
        for num in nums:
            if num == 0:
                j += 1
        if 5 - nums[j] - j > j:
            return False
        return True


if __name__ == '__main__':
    a = Solution()
    print(a.isStraight([1,2,3,4,5]))
