# -*- coding: utf-8 -*-
# @Time    : 2021/1/25 20:27
# @Author  : tmb
from typing import List

'''
题目就是要统计同一时刻进行的最大会议的数量
我们可以把所有的开始时间和结束时间放在一起排序，
用cur表示当前进行的会议数量，遍历排序后的时间数组
如果是开始时间，cur加1，如果是结束时间，cur减一
在遍历的过程中，cur出现的最大值就是需要的房间数。

'''


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        events = [(iv[0], 1) for iv in intervals] + [(iv[1], -1) for iv in intervals]
        events.sort()  # 按照开始时间排序
        print(events)
        ans = cur = 0
        for _, e in events:
            cur += e
            ans = max(ans, cur)
        return ans


if __name__ == '__main__':
    a = Solution()
    print(a.minMeetingRooms([[0, 15], [5, 20], [19, 30]]))
