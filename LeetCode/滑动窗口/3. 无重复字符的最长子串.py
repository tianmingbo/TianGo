# -*- coding: utf-8 -*-
# @Time    : 2021/1/25 20:03
# @Author  : tmb

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        tmp = set()
        n = len(s)
        res = 0
        r = -1  # 右指针
        for i in range(n):
            if i != 0:
                tmp.remove(s[i - 1])  # 左指针，去掉重复元素
            while r + 1 < n and s[r + 1] not in tmp:  # 如果下一个不在滑动窗口中
                tmp.add(s[r + 1])  # 加入滑动窗口
                r += 1  # 右指针右移
            res = max(res, r - i + 1)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.lengthOfLongestSubstring("abcdabcbb"))
