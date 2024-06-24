# -*- coding: utf-8 -*-
# @Time    : 2021/1/26 17:43
# @Author  : tmb
from typing import List


class Solution:
    def subarraySum(self, nums: List[int], key: int) -> int:
        prefix = {}
        counter = 0
        pre_sum = 0  # 前缀和
        for i in range(len(nums)):
            pre_sum += nums[i]  # 前缀和
            if pre_sum == key:  # 如果前缀和等于k
                counter += 1
            if pre_sum - key in prefix:  # 如果 前缀和-k 在prefix中，说明从之前任意元素到目前元素，和为k
                counter += prefix[pre_sum - key]
            if pre_sum in prefix:
                prefix[pre_sum] += 1
            else:
                prefix[pre_sum] = 1
        return counter


if __name__ == '__main__':
    a = Solution()
    print(a.subarraySum([3, 4, 7, 2, -3, 1, 4, 2], 4))
