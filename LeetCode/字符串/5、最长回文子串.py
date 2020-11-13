# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 20:31
# @Author  : tmb


'''
状态转移方程：
dp[i][j] = s[i] == s[j] and ( j -i < 3 or dp[i+1][j-1])
'''


class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) < 2:
            return s
        dp = [[False for _ in range(len(s))] for _ in range(len(s))]
        for i in range(len(s)):
            dp[i][i] = True  # 赋初始值，没有砂卵用
        max_len = 1
        cur = 0
        for j in range(len(s)):  # 优先遍历每列
            for i in range(0, j):
                if s[i] == s[j]:
                    if j - i < 3:  # ’bb‘
                        dp[i][j] = True
                    else:
                        dp[i][j] = dp[i + 1][j - 1]
                else:
                    dp[i][j] = False
                if dp[i][j]:
                    cur_len = j - i + 1  # 计算当前长度
                    if cur_len > max_len:
                        max_len = cur_len
                        cur = i  # 记录回文串的其起始位置
        return s[cur:cur + max_len]


if __name__ == '__main__':
    a = Solution()
    print(a.longestPalindrome('babad'))
