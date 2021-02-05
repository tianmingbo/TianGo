# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 14:07
# @Author  : tmb
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if not n:
            return 1
        if n == 1:
            return x
        fu_flag = False
        if n < 0:
            n = abs(n)
            fu_flag = True
        ji_flag = False

        if n % 2 != 0:
            ji_flag = True

        res = self.myPow(x, n // 2) ** 2

        if ji_flag:
            res *= x
        if fu_flag:
            return 1 / res
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.myPow(2.10000, 3))
