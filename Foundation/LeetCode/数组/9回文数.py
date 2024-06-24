# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 18:01
# @Author  : tmb
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        tmp = 0
        y = x
        while x != 0:
            tmp *= 10
            tmp += x % 10
            x //= 10
        return tmp == y


if __name__ == '__main__':
    a = Solution()
    print(a.isPalindrome(11111111111111111111111111111111111111111111111))
