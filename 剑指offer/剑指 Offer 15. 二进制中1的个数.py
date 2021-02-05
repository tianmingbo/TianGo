# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 14:03
# @Author  : tmb
class Solution:
    def hammingWeight(self, n: int) -> int:
        res = 0
        while n:
            n &= (n - 1)
            res += 1
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.hammingWeight(int(input(), 2)))
