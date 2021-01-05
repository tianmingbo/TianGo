# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 20:33
# @Author  : tmb
class Solution:
    def findNthDigit(self, n: int) -> int:
        i, base, mi = 1, 9, 0
        while n > (i * base * 10 ** mi):
            n -= (i * base * 10 ** mi)
            mi += 1
            i += 1
        start = 10 ** mi
        num = start + (n // i) - 1
        return int(str(num)[i - 1])


if __name__ == '__main__':
    a = Solution()
    print(a.findNthDigit(1000000))
