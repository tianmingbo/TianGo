# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 15:52
# @Author  : tmb
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if not needle:
            return 0
        tmp = []
        for i in range(len(haystack)):
            if haystack[i] == needle[0]:
                tmp.append(i)
        for j in tmp:
            if haystack[j:j + len(needle)] == needle:
                return j
        return -1


if __name__ == '__main__':
    a = Solution()
    print(a.strStr(haystack="mssssppi", needle="issipi"))
