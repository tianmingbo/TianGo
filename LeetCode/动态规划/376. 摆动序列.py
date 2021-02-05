# -*- coding: utf-8 -*-
# @Time    : 2021/1/10 15:49
# @Author  : tmb
from typing import List

'''
画图，求峰值，峰谷
'''


class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:
        # 动态规划
        n = len(nums)
        if n < 2:
            return n

        up = [1] + [0] * (n - 1)
        down = [1] + [0] * (n - 1)
        for i in range(1, n):
            if nums[i] > nums[i - 1]:
                up[i] = max(up[i - 1], down[i - 1] + 1)
                down[i] = down[i - 1]
            elif nums[i] < nums[i - 1]:
                up[i] = up[i - 1]
                down[i] = max(up[i - 1] + 1, down[i - 1])
            else:
                up[i] = up[i - 1]
                down[i] = down[i - 1]
        print(up, down)
        return max(up[n - 1], down[n - 1])

    def wiggleMaxLength2(self, nums: List[int]) -> int:
        # 贪心
        n = len(nums)
        if n < 2:
            return n
        pre_diff = 0
        res = 1  # 记录峰值个数，序列默认序列最右边有一个峰值
        for i in range(1, n):
            cur_diff = nums[i] - nums[i - 1]
            if (cur_diff > 0 >= pre_diff) or (cur_diff < 0 <= pre_diff):
                res += 1
                pre_diff = cur_diff
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.wiggleMaxLength2([1, 2, 2, 2, 4, 5, 6, 4]))
