# -*- coding: utf-8 -*-
# @Time    : 2020/12/4 10:38
# @Author  : tmb
from typing import List


class Solution:
    """
    本题可以理解为背包问题，背包容量为sum(nums)/2，如果sum（nums）为奇数，说明不能正确分割，
    物品个数为n，要求装满背包。
    """

    def canPartition(self, nums: List[int]) -> bool:
        '''

        :param nums:
        :return: [n][sum_nums]=True,可以正确分割，否则不可以
        '''
        if not nums:
            return False
        n = len(nums)
        sum_nums = sum(nums) // 2
        if sum(nums) % 2 != 0:
            return False

        dp = [[False] * (sum_nums + 1) for _ in range(n + 1)]  # 第一维是几个数字（n个物品），第二维是背包容量
        for k in range(n + 1):
            dp[k][0] = True  # 0意味着没有空间，说明背包装满了，为True
        for i in range(1, n + 1):
            for j in range(1, sum_nums + 1):
                # 假设初始dp[3][6] =True,说明对于容量6的背包，若用前3个，有一种方法可以装满
                # dp[i-1][j] 说明第i个物品不装 dp[4][6]
                # dp[i-1][j-nums[i-1]] 第i个物品装 dp[4][9]
                if j - nums[i - 1] < 0:
                    dp[i][j] = dp[i - 1][j]  # 空间不够，不装
                else:
                    dp[i][j] = dp[i - 1][j] | dp[i - 1][j - nums[i - 1]]
        return dp[n][sum_nums]

    def canPartition2(self, nums: List[int]) -> bool:
        ssum = sum(nums)
        if ssum % 2:
            return False
        ssum = ssum // 2
        dp = [False for _ in range(ssum + 1)]
        dp[0] = True
        for i in range(len(nums)):
            for j in range(ssum, nums[i] - 1, -1):
                dp[j] = (dp[j] or dp[j - nums[i]])
        return dp[ssum]


if __name__ == '__main__':
    a = Solution()
    print(a.canPartition([1, 2, 3, 6]))
