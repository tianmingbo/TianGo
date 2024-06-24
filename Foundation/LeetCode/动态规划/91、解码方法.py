# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 17:33
# @Author  : tmb

class Solution:
    def numDecodings(self, s: str) -> int:
        if not s:
            return 0

        dp = [0 for x in range(len(s) + 1)]

        # base case initialization
        dp[0] = 1
        dp[1] = 0 if s[0] == "0" else 1  # (1)
        print(dp)
        for i in range(2, len(s) + 1):
            # One step jump
            if 0 < int(s[i - 1:i]) <= 9:  # (2)
                dp[i] += dp[i - 1]
            # Two step jump
            if 10 <= int(s[i - 2:i]) <= 26:  # (3)
                dp[i] += dp[i - 2]
        print(dp)
        return dp[len(s)]


if __name__ == '__main__':
    a = Solution()
    print(a.numDecodings('01022'))
