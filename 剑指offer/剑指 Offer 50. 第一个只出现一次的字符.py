# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 20:31
# @Author  : tmb
class Solution:
    def firstUniqChar(self, s: str) -> str:
        if not s:
            return ' '
        hash_table = {}
        for i in s:
            if i not in hash_table:
                hash_table[i] = 1
            else:
                hash_table[i] += 1
        for j in range(len(s)):
            if hash_table[s[j]] == 1:
                return s[j]
        return " "


if __name__ == '__main__':
    a = Solution()
    print(a.firstUniqChar("dd"))
