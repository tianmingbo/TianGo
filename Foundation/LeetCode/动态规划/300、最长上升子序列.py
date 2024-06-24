# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 11:42
# @Author  : tmb

'''
我的思路： 1、遍历
2、动态规划，向前寻找比当前小的那个位置，统计那个位置前面比自己小的个数  dp[i]=max(dp[j])+1

'''
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums:
            return 0
        dp = [1 for _ in nums]
        for i in range(1, len(nums)):
            for j in range(i, -1, -1):
                if nums[j] < nums[i]:  # 统计前方所有比当前位置小的元素
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)


import bisect


# 贪心+二分
class Solution2:
    def lengthOfLIS(self, arr):
        if not arr:
            return None
        n = len(arr)
        dp = [1] * n
        helper = [arr[0]]
        for i, a in enumerate(arr[1:], 1):  # 从下标1开始遍历
            if a > helper[-1]:
                helper.append(a)
                dp[i] = len(helper)
            else:
                pos = bisect.bisect_left(helper, a)  # 通过二分，找出当前元素应在的位置
                dp[i] = pos + 1
                helper[pos] = a
        # 上面相当于求出最长公共子串，dp记录最长子串
        length = len(helper)
        for i in range(n - 1, -1, -1):
            if dp[i] == length:
                length -= 1
                helper[length] = arr[i]
        return helper


if __name__ == '__main__':
    a = Solution()
    print(a.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18, 16, 5]))
