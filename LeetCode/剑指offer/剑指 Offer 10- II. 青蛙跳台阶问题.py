# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 21:12
# @Author  : tmb
class Solution:
    def numWays(self, n: int) -> int:
        if not n:
            return 1
        if n == 1:
            return 1
        rec1, rec2 = 1, 2
        for _ in range(3, n + 1):
            rec1, rec2 = rec2, rec1 + rec2
        return rec2 % (10 ** 9 + 7)


if __name__ == '__main__':
    a = Solution()
    print(a.numWays(7))
