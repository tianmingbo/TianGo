# -*- coding: utf-8 -*-
# @Time    : 2020/10/14 9:21
# @Author  : tmb
class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1  # 把最后一位1置0
            count += 1
        return count


if __name__ == '__main__':
    a = Solution()
    a.hammingWeight(int(input(), 2))
