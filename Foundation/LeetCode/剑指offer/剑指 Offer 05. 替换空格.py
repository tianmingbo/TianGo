# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 20:34
# @Author  : tmb
class Solution:
    def replaceSpace(self, s: str) -> str:
        if not s:
            return s
        return s.replace(' ', '%20')


if __name__ == '__main__':
    a = Solution()
    print(a.replaceSpace(s="We are happy."))
