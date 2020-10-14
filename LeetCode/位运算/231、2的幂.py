# -*- coding: utf-8 -*-
# @Time    : 2020/10/14 9:34
# @Author  : tmb
class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        if not n:
            return False
        return (n & (n - 1)) == 0  # 是2的幂，则二进制只有1位1


if __name__ == '__main__':
    a = Solution()
    print(a.isPowerOfTwo(1))
