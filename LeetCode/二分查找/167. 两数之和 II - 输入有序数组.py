# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 10:16
# @Author  : tmb
from typing import List

'''
双指针
'''


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        low, high = 0, len(numbers) - 1
        while low <= high:
            if numbers[low] + numbers[high] == target:
                return [low + 1, high + 1]
            if numbers[low] + numbers[high] < target:
                low += 1
            if numbers[low] + numbers[high] > target:
                high -= 1
        return [-1, -1]


if __name__ == '__main__':
    a = Solution()
    print(a.twoSum(numbers=[2, 7, 11, 15], target=9))
