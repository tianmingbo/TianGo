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
        cur_sum = 0
        start = 0
        for i in range(len(gas)):
            cur_sum += gas[i] - cost[i]
            if cur_sum < 0:  # 如果当前油不够跑到下一个加油站，则0~i都不作为起点
                start = i + 1
                cur_sum = 0
        return start


if __name__ == '__main__':
    a = Solution()
    print(a.canCompleteCircuit2(gas=[3, 1, 1],
                                cost=[1, 2, 2]))
