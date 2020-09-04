# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 15:01
# @Author  : tmb

class Solution:
    def isUnique(self, astr: str) -> bool:
        n = 0
        for i in astr:
            print(n^1)
            new = n ^ 1 << (ord(i) - 97)
            if new < n:
                return False
            n = new
        return True


if __name__ == '__main__':
    a = Solution()
    print(a.isUnique('leetcode'))
