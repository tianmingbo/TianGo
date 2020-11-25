# -*- coding: utf-8 -*-
# @Time    : 2020/11/25 18:32
# @Author  : tmb
from typing import List

'''
https://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247484493&idx=1&sn=1615b8a875b770f25875dab54b7f0f6f&chksm=9bd7fa45aca07353a347b7267aaab78b81502cf7eb60d0510ca9109d3b9c0a1d9dda10d99f50&scene=21#wechat_redirect
'''


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0
        intervals = sorted(intervals, key=lambda i: i[1])  # 对结束排序
        count = 1
        x_end = intervals[0][1]  # 初始结束值
        for i in range(len(intervals)):
            if intervals[i][0] >= x_end:  # 如果下一个的开始值大于初始值，则证明没有相交
                count += 1
                x_end = intervals[i][1]  # 更新初始值
        return len(intervals) - count


if __name__ == '__main__':
    a = Solution()
    print(a.eraseOverlapIntervals([[1, 2], [2, 5], [1, 5]]))
