#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/3/2 20:03
    @Describe  BFS
"""
from typing import List


class Solution:
    def subtraction(self, i):
        if i == '0':
            return '9'
        else:
            return str(int(i) - 1)

    def _add(self, i):
        if i == '9':
            return '0'
        else:
            return str(int(i) + 1)

    def openLock(self, deadends: List[str], target: str) -> int:
        deadends = set(deadends)
        import collections
        queue = collections.deque()
        queue.append(('0000', 0))
        visited = {'0000'}
        while queue:
            w, step = queue.popleft()
            if w == target:
                return step
            if w in deadends:
                continue
            for i in range(len(w)):
                tmp1 = w[:i] + self._add(w[i]) + w[i + 1:]
                tmp2 = w[:i] + self.subtraction(w[i]) + w[i + 1:]
                if tmp1 not in visited:
                    visited.add(tmp1)
                    queue.append((tmp1, step + 1))
                if tmp2 not in visited:
                    visited.add(tmp2)
                    queue.append((tmp2, step + 1))
        return -1


if __name__ == '__main__':
    a = Solution()
    print(a.openLock(deadends=["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], target="8888"))
