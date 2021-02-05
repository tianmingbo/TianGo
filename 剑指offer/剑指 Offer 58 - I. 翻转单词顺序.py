# -*- coding: utf-8 -*-
# @Time    : 2021/1/8 20:18
# @Author  : tmb
class Solution:
    def reverseWords(self, s: str) -> str:
        s = s.strip()
        tmp = []
        l, r = 0, 0
        for j in range(len(s)):
            if s[j] != ' ':
                r += 1
            else:
                tmp.append(s[l:r])
                r += 1
                l = r
        tmp.append(s[l:r])
        return ' '.join([i for i in tmp if i != ''][::-1])


if __name__ == '__main__':
    a = Solution()
    print(a.reverseWords("a good   example"))
