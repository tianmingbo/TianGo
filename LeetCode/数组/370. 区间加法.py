"""
假设你有一个长度为n的数组，初始情况下所有的数字均为0，你将会被给出k个更新的操作。

其中，每个操作会被表示为一个三元组：[startIndex, endIndex, inc]，你需要将子数组A[startIndex ... endIndex]（包括 startIndex 和 endIndex）增加inc。

请你返回k次操作后的数组。

示例:

输入: length = 5, updates = [[1,3,2],[2,4,3],[0,2,-2]]
输出: [-2,0,3,5,3]
解释:

初始状态:
[0,0,0,0,0]

进行了操作 [1,3,2] 后的状态:
[0,2,2,2,0]

进行了操作 [2,4,3] 后的状态:
[0,2,5,5,3]

进行了操作 [0,2,-2] 后的状态:
[-2,0,3,5,3]

"""
from typing import List


# 差分数组
class Solution:
    diff = []
    length = 0
    res = []

    def getModifiedArray(self, length: int, updates: List[List[int]]) -> List[int]:
        self.diff = [0 for _ in range(length)]
        self.res = [0 for _ in range(length)]
        self.length = length
        for update in updates:
            self.increment(update[0], update[1], update[2])
        self.result()
        return self.res

    def increment(self, start, end, val):
        self.diff[start] += val
        if end + 1 < self.length:
            self.diff[end + 1] -= val

    def result(self):
        self.res[0] = self.diff[0]
        for i in range(1, len(self.diff)):
            self.res[i] = self.res[i - 1] + self.diff[i]


if __name__ == '__main__':
    so = Solution()
    print(so.getModifiedArray(length=5, updates=[[1, 3, 2], [2, 4, 3], [0, 2, -2]]))
