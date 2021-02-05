# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 15:14
# @Author  : tmb
class Solution:
    def maxProduct(self, nums) -> int:
        if len(nums) == 1:
            return nums[0]
        dp = [[0] * 2 for _ in range(len(nums))]
        # 存储最大值
        dp[0][0] = nums[0]
        # 存储最小值
        dp[0][1] = nums[0]
        res = max(dp[0])
        for i in range(1, len(nums)):
            dp_0 = dp[i - 1][0] * nums[i]
            dp_1 = dp[i - 1][1] * nums[i]
            dp[i][0] = max(dp_0, dp_1, nums[i])  # 保存最大值
            dp[i][1] = min(dp_0, dp_1, nums[i])  # 保存最小值，最大值乘以负数，变成最小值
            res = max(res, dp[i][0], dp[i][1])
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.maxProduct([2, -1, -2, 1]))
