# -*- coding: utf-8 -*-
# @Time    : 2020/11/6 21:14
# @Author  : tmb
class Solution:
    def reverseStr(self, s: str, k: int) -> str:
        a = list(s)
        for i in range(0, len(s), 2 * k):
            a[i:i + k] = reversed(a[i:i + k])
        return ''.join(a)


if __name__ == '__main__':
    a = Solution()
    print(a.reverseStr('tianmingbo', 2))
