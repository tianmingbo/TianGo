# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 17:27
# @Author  : tmb

'''
转移方程：
dp[i] = max(nums[i], dp[i - 1] + nums[i])
'''


class Solution:
    def maxSubArray(self, nums):
        if not nums:
            return 0
        dp = [0 for _ in nums]
        for i in range(len(nums)):
            dp[i] = max(nums[i], dp[i - 1] + nums[i])
        return max(dp)


if __name__ == '__main__':
    a = Solution()
    print(a.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
