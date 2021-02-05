# -*- coding: utf-8 -*-
# @Time    : 2020/10/14 9:44
# @Author  : tmb
class Solution:
    def reverseBits(self, n: int) -> int:
        ret, power = 0, 31
        while n:
            ret += (n & 1) << power  # n&1,左移31位
            n = n >> 1  # n右移1位
            power -= 1
        return ret


if __name__ == '__main__':
    a = Solution()
    a.reverseBits(int(input(), 2))
    # 10000010100101000001111010011100
    # 111001011110000010100101000001
