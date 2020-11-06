# -*- coding: utf-8 -*-
# @Time    : 2020/11/6 22:22
# @Author  : tmb
class Solution:
    def reverseWords(self, s: str) -> str:
        import collections
        d, tmp = collections.deque(), []
        for i in s:
            if i != " ":
                tmp.append(i)
            else:
                for j in tmp[::-1]:
                    d.append(j)
                tmp = []
                d.append(' ')
        for j in tmp[::-1]:
            d.append(j)
        return ''.join(d)


if __name__ == '__main__':
    a = Solution()
    print(a.reverseWords("Let's take LeetCode contest"))
