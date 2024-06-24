# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 20:06
# @Author  : tmb
from typing import List


class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if not nums:
            return None
        i = len(nums) - 1
        j = -1  # j=-1 如果是 54321这样
        while i > 0:
            if nums[i - 1] < nums[i]:  # 找到第一个前面小于后面的index
                j = i - 1
                break
            i -= 1
        for i in range(len(nums) - 1, -1, -1):
            if nums[i] > nums[j]:  #
                nums[i], nums[j] = nums[j], nums[i]  # 交换找到的前面的元素小于后面的
                nums[j + 1:] = sorted(nums[j + 1:])  # 之后的元素排序
                return


if __name__ == '__main__':
    a = Solution()
    a.nextPermutation([5, 1, 5, 5, 4])
