# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 20:31
# @Author  : tmb


'''
状态转移方程：
dp[i][j] = s[i] == s[j] and ( j -i < 3 or dp[i+1][j-1])
'''


class Solution:
    def expandAroundCenter(self, s, left, right):
        # 在 s 中寻找以 s[l] 和 s[r] 为中心的最长回文串
        while left >= 0 and right < len(s) and s[left] == s[right]:
            # 双指针，向两边展开
            left -= 1
            right += 1
        return left + 1, right - 1

    def longestPalindrome(self, s: str) -> str:
        start, end = 0, 0
        for i in range(len(s)):
            left1, right1 = self.expandAroundCenter(s, i, i)  # 以 s[i] 为中心的最长回文子串
            left2, right2 = self.expandAroundCenter(s, i, i + 1)  # 以 s[i] 和 s[i+1] 为中心的最长回文子串
            if right1 - left1 > end - start:
                start, end = left1, right1
            if right2 - left2 > end - start:
                start, end = left2, right2
        return s[start: end + 1]


if __name__ == '__main__':
    a = Solution()
    print(a.longestPalindrome('babab'))
