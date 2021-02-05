# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 19:04
# @Author  : tmb
class Solution:
    def strToInt(self, strs: str) -> int:

        res, sign = 0, 1
        strs = strs.strip()
        for i in range(len(strs)):
            ch = strs[i]
            if i == 0 and (ch == '-' or ch == '+'):
                if ch == '-':
                    sign = -1
                if ch == '+':
                    sign = 1
                continue
            if not ch.isdigit():
                break
            res = res * 10 + ord(ch) - ord('0')
        if res * sign < -2 ** 31:
            return -2 ** 31
        if res * sign > 2 ** 31 - 1:
            return 2 ** 31 - 1
        return sign * res


if __name__ == '__main__':
    a = Solution()
    print(a.strToInt(" "))
