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
            if left_n == n and right_n == n:  # 终结条件，如果左括号和右括号都用完了
                res.append(''.join(path[:]))
            if left_n < n:  # 左括号没有用完
                path.append('(')
                dfs(left_n + 1, right_n, path)
                path.pop()
            if right_n < left_n:  # 剪枝，如果当前右括号个数小于左括号，说明再往下的括号不符合题意
                path.append(')')
                dfs(left_n, right_n + 1, path)
                path.pop()

        dfs(0, 0, [])
        return res

    def generateParenthesis2(self, n: int) -> List[str]:
        if n == 0:
            return []
        res = []
        s = ''

        def _generate(left, right, s):
            if right == n and left == n:
                res.append(s)
                return
            if left < n:
                _generate(left + 1, right, s + '(')
            if right < left:
                _generate(left, right + 1, s + ')')

        _generate(0, 0, s)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.generateParenthesis(3))
