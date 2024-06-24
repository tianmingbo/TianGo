# -*- coding: utf-8 -*-
# @Time    : 2020/9/12 13:16
# @Author  : tmb
class Solution:
    def jump(self, nums) -> int:
        n = len(nums)
        maxPos, end, step = 0, 0, 0
        for i in range(n - 1):
            if maxPos >= i:
                maxPos = max(maxPos, i + nums[i])
                if i == end:
                    end = maxPos
                    step += 1
        return step


if __name__ == '__main__':
    a = Solution()
    print(a.jump([2, 3, 1, 1, 4]))
