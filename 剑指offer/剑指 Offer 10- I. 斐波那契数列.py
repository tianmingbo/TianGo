# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 21:07
# @Author  : tmb
class Solution:
    def fib(self, n: int) -> int:
        if not n:
            return 0
        rec1, rec2 = 1, 1
        for i in range(2, n):
            rec1, rec2 = rec2, rec1 + rec2
        return rec2 % (10 ** 9 + 7)


if __name__ == '__main__':
    a = Solution()
    print(a.fib(5))
