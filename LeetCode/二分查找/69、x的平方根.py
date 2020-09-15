# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 14:13
# @Author  : tmb
# 二分法，
class Solution:
    def mySqrt(self, x: int) -> int:
        left = 0
        right = x
        ans = -1
        while (left <= right):
            mid = (left + right) // 2
            if mid ** 2 <= x:
                left = mid + 1
                ans = mid
            else:
                right = mid - 1
        return ans


class Solution2:
    # 牛顿迭代法
    def mySqrt(self, x: int) -> int:
        if x == 0:
            return 0

        C, x0 = float(x), float(x)
        while True:
            xi = 0.5 * (x0 + C / x0)
            if abs(x0 - xi) < 1e-7:
                break
            x0 = xi

        return int(x0)


if __name__ == '__main__':
    a = Solution2()
    print(a.mySqrt(4))
