# -*- coding: utf-8 -*-
# @Time    : 2020/11/25 21:43
# @Author  : tmb
from typing import List


class Solution:
    '''
    空间复杂度O(1)，时间复杂度O(n)
    '''

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        if not nums:
            return []
        res = [0 for _ in range(len(nums))]  # 初始化res
        tmp = 1
        for i in range(len(nums)):  # 从左往右，存储当前元素的左边的乘积
            res[i] = tmp
            tmp *= nums[i]
        tmp = 1
        for j in range(len(nums) - 1, -1, -1):  # 从右向左，乘以当前元素的右边
            res[j] *= tmp
            tmp *= nums[j]
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.productExceptSelf([1, 2, 3, 4]))
