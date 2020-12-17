# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 17:13
# @Author  : tmb
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        if not s:
            return 0
        dp = [0 for _ in range(len(s))]
        dp[0] = 0
        for i in range(1, len(dp)):
            if s[i] == '(':
                dp[i] = 0

            elif s[i] == ')':
                if s[i - 1] == '(':
                    if i - 2 >= 0:
                        dp[i] = dp[i - 2] + 2
                    else:
                        dp[i] = 2
                elif s[i - 1] == ')' and i - dp[i - 1] - 1 >= 0 and s[i - dp[i - 1] - 1] == '(':
                    dp[i] = dp[i - 1] + dp[i - dp[i - 1] - 2] + 2
        return max(dp)


if __name__ == '__main__':
    a = Solution()
    print(a.longestValidParentheses("()(())"))
