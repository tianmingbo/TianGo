# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 10:00
# @Author  : tmb
'''
使用纵向扫描，f,f,f,l,l,l
'''


class Solution:
    def longestCommonPrefix(self, strs):
        if not strs:
            return ""
        max_short = min(strs, key=len)
        for index, value in enumerate(max_short):
            for i in strs:
                if i[index] != value:
                    return max_short[:index]
        return max_short

if __name__ == '__main__':
    a = Solution()
    print(a.longestCommonPrefix([""]))
