# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 17:21
# @Author  : tmb
class Solution:
    '''
    动态规划，当走到这一间时，可以考虑这一间偷不偷，如果偷前一间的钱之和 比 偷这一间和前两间的和 大，
    就偷这一间
    '''

    def rob(self, nums) -> int:
        if not nums:
            return 0
        if len(nums) <= 2:
            return max(nums)
        dp = [0 for i in nums]
        dp[0] = nums[0]
        dp[1] = max(nums[1], nums[0])
        for i in range(2, len(nums)):
            dp[i] = max(dp[i - 2] + nums[i], dp[i - 1])
        print(dp)
        return max(dp)


class Solution2:
    '''
    滚动数组，
    '''

    def rob(self, nums) -> int:
        if not nums:
            return 0

        size = len(nums)
        if size == 1:
            return nums[0]

        first, second = nums[0], max(nums[0], nums[1])
        for i in range(2, size):
            first, second = second, max(first + nums[i], second)

        return second


if __name__ == '__main__':
    a = Solution()
    print(a.rob([2, 1, 1, 2]))
