# -*- coding: utf-8 -*-
# @Time    : 2021/1/18 21:33
# @Author  : tmb
from typing import List


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        dct = {}
        for i in range(len(nums)):
            if nums[i] in dct and dct[nums[i]] >= i - k:
                return True
            dct[nums[i]] = i
        return False


if __name__ == '__main__':
    a = Solution()
    print(a.containsNearbyDuplicate(nums=[1, 2, 3, 4, 5, 6, 7, 8, 9, 9], k=3))
