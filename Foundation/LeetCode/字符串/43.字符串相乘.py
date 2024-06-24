# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 17:14
# @Author  : tmb
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == '0' or num2 == '0':
            return '0'
        tmp1, tmp2 = 0, 0
        for i in range(len(num1)):
            tmp1 += (ord(num1[i]) - ord('0')) * 10 ** (len(num1) - i - 1)
        for i in range(len(num2)):
            tmp2 += (ord(num2[i]) - ord('0')) * 10 ** (len(num2) - i - 1)
        return str(tmp2 * tmp1)


if __name__ == '__main__':
    a = Solution()
    print(a.multiply('123', '0'))
