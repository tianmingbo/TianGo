# -*- coding: utf-8 -*-
# @Time    : 2021/1/20 21:33
# @Author  : tmb
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = -1, -1
        left_max, right_max = [], []
        for i in range(len(height)):  # 从左向右，找到最大值
            if height[i] > left:
                left = height[i]
                left_max.append(left)
            else:
                left_max.append(left)
        for j in range(len(height) - 1, -1, -1):  # 从右向左，找到最大值
            if height[j] > right:
                right = height[j]
                right_max.append(right)
            else:
                right_max.append(right)
        print(left_max,right_max)
        # sum(left_max) + sum(right_max) 多加了一个矩阵的面积，right * len(height)是整个矩阵的面积
        return sum(left_max) + sum(right_max) - sum(height) - right * len(height)


if __name__ == '__main__':
    a = Solution()
    print(a.trap(height=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
