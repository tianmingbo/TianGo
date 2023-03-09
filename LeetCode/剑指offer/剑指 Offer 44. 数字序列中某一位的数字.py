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
        num = start + ((n - 1) // i)
        index = (n - 1) % i
        return int(str(num)[index])


class Solution2:
    def findNthDigit(self, n: int) -> int:
        num = 9
        cnt = 1
        # 计算n在哪个区间
        while n > num * cnt:
            n -= num * cnt
            cnt += 1
            num *= 10
        # 计算目标数
        target = num // 9 + (n - 1) // cnt
        print(n)
        # 计算在目标数的第几位
        index = (n - 1) % cnt
        return int(str(target)[index])


if __name__ == '__main__':
    a = Solution2()
    print(a.findNthDigit(1000000))
