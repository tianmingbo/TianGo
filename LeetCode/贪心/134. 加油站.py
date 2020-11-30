# -*- coding: utf-8 -*-
# @Time    : 2020/11/26 10:20
# @Author  : tmb
from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        left = [gas[i] - cost[i] for i in range(len(gas))]
        minValue = 999
        minIndex = 0

        sumValue = 0
        for j, l in enumerate(left):
            sumValue += l
            if sumValue < minValue:
                minValue = sumValue
                minIndex = j

        if sumValue < 0:
            return -1
        else:
            return (minIndex + 1) % len(gas)

    def canCompleteCircuit2(self, gas: List[int], cost: List[int]) -> int:
        if sum(cost) > sum(gas):
            return -1
        left = [gas[i] - cost[i] for i in range(len(gas))]
        print(left)
        start = 0
        for i in left:
            if i < 0:
                start += 1
        return start


if __name__ == '__main__':
    a = Solution()
    print(a.canCompleteCircuit([5, 1, 2, 3, 4]
                                , [4, 4, 1, 5, 1]))
