# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 16:08
# @Author  : tmb
class Solution:
    def reverse(self, x: int) -> int:
        res = 0
        flag = True
        if x < 0:
            flag = False  # x<0
            x = abs(x)
        while (x != 0):
            tmp = x % 10
            if res > 214748364 or (res > 214748364 and tmp > 7):  # 2**31==2147483648
                return 0
            res = res * 10 + tmp
            x //= 10
        if not flag:
            return -res
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.reverse(1463847412))
