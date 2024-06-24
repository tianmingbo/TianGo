# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 18:25
# @Author  : tmb

class Solution:
    def isNumber(self, s: str) -> bool:
        if not s:
            return False
        for i in range(len(s)):
            if s[i].isalpha():  # 判断是不是字母
                if s[i] != 'e':
                    return False
            if s[i] in ['+', '-']:
                if not s[i + 1].isalnum():
                    return False


if __name__ == '__main__':
    a = Solution()
    print(a.isNumber('abc'))
