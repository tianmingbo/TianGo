# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 22:45
# @Author  : tmb
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        dp = [False for _ in range(len(s) + 1)]
        dp[0] = True  # 0位置为空，可以拆分
        for i in range(1, len(s) + 1):
            for word in wordDict:
                if dp[i - len(word)] and s[i - len(word):i] == word and i - len(word) >= 0:
                    dp[i] = True
        return dp[-1]


if __name__ == '__main__':
    a = Solution()
    print(a.wordBreak(s="leetcode", wordDict=["leet", "code"]))  # dp[3],dp[7]=True
