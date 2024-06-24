# -*- coding: utf-8 -*-
# @Time    : 2020/9/12 10:49
# @Author  : tmb
class Solution:
    def findContentChildren(self, g, s) -> int:
        if not g or not s:
            return 0
        g.sort()
        s.sort()
        i = j = 0
        count = 0
        # 先给最小需求的发饼干，胖的需要减肥
        while i <= len(g) - 1 and j <= len(s) - 1:
            if g[i] <= s[j]:
                count += 1
                i += 1
            j += 1
        return count


if __name__ == '__main__':
    a = Solution()
    print(a.findContentChildren([10, 9, 8, 7],
                                [5, 6, 7, 8]
                                ))
