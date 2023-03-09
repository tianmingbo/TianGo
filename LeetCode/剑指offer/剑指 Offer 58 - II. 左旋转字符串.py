# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 19:28
# @Author  : tmb
class Solution:
    def reverseLeftWords(self, s: str, n: int) -> str:
        n = n % len(s)
        return s[n:] + s[:n]


if __name__ == '__main__':
    a = Solution()
    print(a.reverseLeftWords("abcdefg", 6))
