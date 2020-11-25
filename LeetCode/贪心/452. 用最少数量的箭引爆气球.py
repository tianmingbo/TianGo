# -*- coding: utf-8 -*-
# @Time    : 2020/11/25 21:16
# @Author  : tmb
from typing import List


class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        if not points:
            return 0
        points = sorted(points, key=lambda i: i[1])  # 类似无重叠区间
        arrow = 1
        cur_end = points[0][1]
        for i in range(1, len(points)):
            if points[i][0] > cur_end:
                arrow += 1
                cur_end = points[i][1]
        return arrow


if __name__ == '__main__':
    a = Solution()
    print(a.findMinArrowShots(points=[[10, 16], [2, 8], [1, 7], [7, 12]]))
