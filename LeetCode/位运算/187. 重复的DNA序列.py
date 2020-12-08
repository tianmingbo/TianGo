# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 15:03
# @Author  : tmb
from typing import List


class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        one, n = 10, len(s)
        res, middle = set(), set()
        for i in range(n - one + 1):
            tmp = s[i:one + i]
            if tmp in middle:
                res.add(tmp)
            middle.add(tmp)
        return list(res)


if __name__ == '__main__':
    a = Solution()
    print(a.findRepeatedDnaSequences(s="AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"))
