# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 17:00
# @Author  : tmb

'''
我的思路：变成一维数组，二分查找。时间复杂度O(logn)，空间O(mn)
'''


class Solution:
    def searchMatrix(self, matrix, target: int) -> bool:
        if not matrix:
            return False
        tmp = [j for i in matrix for j in i]
        print(tmp)
        left, right = 0, len(tmp) - 1
        while left <= right:
            mid = (left + right) // 2
            if tmp[mid] == target:
                return True
            if tmp[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return False


class Solution2:
    def searchMatrix(self, matrix, target):
        # 空间复杂度O(1)
        rows, cols = len(matrix), len(matrix[0])
        low, high = 0, rows * cols - 1
        while low <= high:
            mid = (low + high) // 2
            num = matrix[mid // cols][mid % cols]  # 几行几列
            if num == target:
                return True
            elif num < target:
                low = mid + 1
            else:
                high = mid - 1
        return False


if __name__ == '__main__':
    a = Solution2()
    print(a.searchMatrix(matrix=[[-10, -8, -6, -4, -3], [0, 2, 3, 4, 5], [8, 9, 10, 10, 12]], target=13))
