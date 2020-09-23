# -*- coding: utf-8 -*-
# @Time    : 2020/9/18 9:42
# @Author  : tmb
class Solution:
    def rob(self, nums) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])
        self.dp = [0 for _ in nums]
        return max(self.get_max(nums[:-1]), self.get_max(nums[1:]))  # 抢第一间房子和抢最后一件房子的最大值，不能同时抢

    def get_max(self, rod_house):
        self.dp[0] = rod_house[0]
        self.dp[1] = max(rod_house[0], rod_house[1])
        for i in range(2, len(rod_house)):
            self.dp[i] = max(self.dp[i - 2] + rod_house[i], self.dp[i - 1])
        return max(self.dp)


class Solution2:
    def rob(self, nums: [int]) -> int:
        def my_rob(nums):
            cur, pre = 0, 0
            for num in nums:
                cur, pre = max(pre + num, cur), cur
            return cur

        return max(my_rob(nums[:-1]), my_rob(nums[1:])) if len(nums) != 1 else nums[0]


if __name__ == '__main__':
    a = Solution()
    print(a.rob([0]))
