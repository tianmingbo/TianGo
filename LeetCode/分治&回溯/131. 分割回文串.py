# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 10:24
# @Author  : tmb
from typing import List


class Solution:

    def ishuiwen(self, s):  # 判断回文
        for i in range(len(s) // 2):
            if s[i] != s[-i - 1]:
                return False
        return True

    def partition(self, s: str) -> List[List[str]]:
        if not s:
            return []
        res = []

        def backtrack(s, tmp):
            if not s:  # 遍历到根
                res.append(tmp[:])
                return

            for i in range(1, len(s) + 1):
                if self.ishuiwen(s[:i]):  # 判断是不是回文，不是回文，停止向下
                    tmp.append(s[:i])
                    backtrack(s[i:], tmp)
                    tmp.pop()

        backtrack(s, [])
        return res


'''
#遍历树，第一次选一个，如下为例，左子树可选a-a-b，中间的为aa-b，右子树为aab
'''

if __name__ == '__main__':
    a = Solution()
    print(a.partition('aab'))
