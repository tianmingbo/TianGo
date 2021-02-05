# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 10:08
# @Author  : tmb
from typing import List


class Solution:
    '''
    my:O(nlogn),太慢
    '''

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix:
            return False
        for i in matrix:
            flag = self.search_line(i, target)
            if flag:
                return True
        return False

    def search_line(self, nums, target):
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return True
            if nums[mid] > target:
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
        return False

    def searchMatrix2(self, matrix: List[List[int]], target: int) -> bool:
        '''
        解法二 O(m+n)
        :param matrix:
        :param target:
        :return:
        '''
        if not matrix:
            return False
        x, y = 0, len(matrix[0]) - 1
        while x <= len(matrix) - 1 and y >= 0:
            if matrix[x][y] == target:
                return True
            elif target > matrix[x][y]:
                x += 1
            else:
                y -= 1
        return False


if __name__ == '__main__':
    a = Solution()
    print(a.searchMatrix2(
        matrix=[[1, 4, 7, 11, 15],
                [2, 5, 8, 12, 19],
                [3, 6, 9, 16, 22],
                [10, 13, 14, 17, 24],
                [18, 21, 23, 26, 30]],
        target=18))
