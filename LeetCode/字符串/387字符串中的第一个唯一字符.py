# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 14:48
# @Author  : tmb

class Solution:
    def firstUniqChar(self, s: str) -> int:
        if not s:
            return -1
        import collections
        tmp = collections.OrderedDict()
        for index, elem in enumerate(s):
            if elem in tmp.keys():
                tmp[elem] += 1
            else:
                tmp[elem] = 1
        for k,v in tmp.items():
            if v == 1:
                return s.index(k)
        return -1

class Solution2:
    def firstUniqChar(self, s: str) -> int:
        from collections import Counter
        c = Counter(s)
        print(c)
        for key in c:
            if c[key] == 1:
                return s.find(key)

        return -1

if __name__ == '__main__':
    a = Solution2()
    print(a.firstUniqChar('leetcode'))
