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

    def greedy(self, nums):
        if not nums:
            return 0
        count = 0
        res = -float('inf')
        for i in range(len(nums)):
            count += nums[i]  # 不能让“连续和”为负数的时候加上下一个元素，而不是 不让“连续和”加上一个负数
            if count > res:
                res = count
            if count <= 0:
                count = 0
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.greedy([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
