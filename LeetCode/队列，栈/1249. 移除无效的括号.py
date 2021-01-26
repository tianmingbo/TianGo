# -*- coding: utf-8 -*-
# @Time    : 2021/1/25 21:00
# @Author  : tmb
class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        if not s:
            return s
        res = list(s)
        stack = []
        for i in range(len(s)):  # 栈
            if not stack and s[i] == ')':
                res.remove(s[i])
            if stack and s[i] == ')':
                stack.pop()
            if s[i] == '(':
                stack.append('(')
        # 删除没有匹配的左括号
        num = len(stack)
        for j in range(len(res) - 1, -1, -1):
            if not num:
                break
            if res[j] == '(':
                res.pop(j)
                num -= 1
        return ''.join(res)


if __name__ == '__main__':
    a = Solution()
    print(a.minRemoveToMakeValid("(a(b(c)d)"))
