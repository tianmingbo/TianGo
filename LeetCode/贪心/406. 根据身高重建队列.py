# -*- coding: utf-8 -*-
# @Time    : 2021/1/10 19:02
# @Author  : tmb
from typing import List
import collections


class Solution:
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        if not people:
            return []
        people.sort(key=lambda x: (x[0], -x[1]))  # 按照身高排序
        n = len(people)
        ans = [[] for _ in range(n)]
        for person in people:
            spaces = person[1] + 1
            for i in range(n):
                if not ans[i]:
                    spaces -= 1
                    if spaces == 0:
                        ans[i] = person
                        break
        return ans

    def reconstructQueue2(self, people: List[List[int]]) -> List[List[int]]:
        people.sort(key=lambda x: (-x[0], x[1]))
        result = collections.deque()
        for item in people:
            result.insert(item[1], item)
        return list(result)


if __name__ == '__main__':
    a = Solution()
    print(a.reconstructQueue2([[9, 0], [7, 0], [1, 9], [3, 0], [2, 7], [5, 3], [6, 0], [3, 4], [6, 2], [5, 2]]))
