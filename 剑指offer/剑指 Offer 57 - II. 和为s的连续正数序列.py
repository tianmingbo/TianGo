# -*- coding: utf-8 -*-
# @Time    : 2021/1/8 19:23
# @Author  : tmb
from typing import List


class Solution:
    def findContinuousSequence(self, target: int) -> List[List[int]]:
        l, r = 1, 1  # 滑动窗口
        count = 0
        res = []
        while l <= (target // 2):
            if count < target:
                count += r  # 右边界
                r += 1
            elif count > target:
                count -= l  # 左边界
                l += 1
            else:
                res.append(list(range(l, r)))
                count -= l
                l += 1
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.findContinuousSequence(9))
