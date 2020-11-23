# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 20:34
# @Author  : tmb
from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        if not n:
            return []
        res = []

        def dfs(left_n, right_n, path):
            if left_n == n and right_n == n:
                res.append(''.join(path[:]))
            if left_n < n:
                path.append('(')
                dfs(left_n + 1, right_n, path)
                path.pop()
            if right_n < left_n:
                path.append(')')
                dfs(left_n, right_n + 1, path)
                path.pop()

        dfs(0, 0, [])
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.generateParenthesis(3))
