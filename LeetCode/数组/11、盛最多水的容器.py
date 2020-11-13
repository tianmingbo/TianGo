# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 21:06
# @Author  : tmb
class Solution:
    def maxArea(self, height) -> int:
        left, right = 0, len(height) - 1
        max = -float('inf')
        while left <= right:
            tmp = (right - left) * min(height[left], height[right])
            if tmp > max:
                max = tmp
            if height[left] >= height[right]:
                right -= 1
            else:
                left += 1
        return max


if __name__ == '__main__':
    a = Solution()
    print(a.maxArea([1, 10, 6, 2, 5, 4, 10, 3, 7]))
