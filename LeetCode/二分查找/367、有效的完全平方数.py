# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 15:23
# @Author  : tmb
class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        left, right = 0, num
        while left <= right:
            mid = (left + right) // 2
            if mid ** 2 == num:
                return True
            if mid ** 2 < num:
                left = mid + 1
            else:
                right = mid - 1
        return False


if __name__ == '__main__':
    a = Solution()
    print(a.isPerfectSquare(15))
