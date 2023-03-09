# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 18:51
# @Author  : tmb
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        slide_window = set()
        right_point, ans = -1, 0
        n = len(s)
        for i in range(n):
            if i != 0:
                # 每次移除一个字符
                slide_window.remove(s[i - 1])
            while right_point + 1 < n and s[right_point + 1] not in slide_window:
                slide_window.add(s[right_point + 1])
                right_point += 1
            # i到right_point 是无重复的字符串
            ans = max(ans, right_point - i + 1)
        return ans


if __name__ == '__main__':
    a = Solution()
    print(a.lengthOfLongestSubstring("abcabcbb"))
