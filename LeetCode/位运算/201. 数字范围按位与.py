# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 14:18
# @Author  : tmb
class Solution:
    def rangeBitwiseAnd(self, m: int, n: int) -> int:
        while m < n:
            n = n & (n - 1)
        return n


if __name__ == '__main__':
    a = Solution()
    print(a.rangeBitwiseAnd(1,
                            2147483647))
