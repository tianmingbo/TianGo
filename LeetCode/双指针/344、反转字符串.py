# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 14:39
# @Author  : tmb

# 双指针
class Solution:
    def reverseString(self, s):
        i = 0
        j = len(s) - 1
        while i < j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1


if __name__ == '__main__':
    a = Solution()
    a.reverseString(["h", "e", "l", "l", "o"])
