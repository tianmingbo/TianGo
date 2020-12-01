# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 19:40
# @Author  : tmb

class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        # 总体思路就是每次减去divisor的2^n次倍数
        positive = (dividend < 0) is (divisor < 0)  # 一个符号时为False
        dividend, divisor = abs(dividend), abs(divisor)
        res = 0
        while dividend >= divisor:
            temp, i = divisor, 1
            while dividend >= temp:
                dividend -= temp
                res += i
                i <<= 1  # 2^n倍
                temp <<= 1  # temp是divisor的2^n倍
        if not positive:
            res = -res
        return min(max(-2147483648, res), 2147483647)


if __name__ == '__main__':
    a = Solution()
    print(a.divide(100, 3))
