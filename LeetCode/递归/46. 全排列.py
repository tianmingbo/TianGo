# -*- coding: utf-8 -*-
# @Time    : 2020/11/18 11:49
# @Author  : tmb
"""
Level0: []
level1: [1]                  [2]              [3]
level2: [1,2]    [1,3]       [2,1] [2,3]      [3,1] [3,2]
level3: [1,2,3]  [1,3,2]     [2,1,3][2,3,1]   [3,1,2][3,2,1]

"""


class Solution:
    def permute(self, nums):
        if not nums:
            return []
        res = []

        def backtrack(nums, tmp):
            # 终结条件
            if len(tmp) == len(nums):
                res.append(tmp[:])
                return
            for i in range(len(nums)):
                if nums[i] in tmp:  # 添加过滤条件
                    continue
                # 选择
                tmp.append(nums[i])
                # 回溯
                backtrack(nums, tmp)
                # 撤销选择
                tmp.pop()

        backtrack(nums, [])
        return res


from typing import List


class Solution2:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def dfs(nums, size, depth, path, used, res):
            if depth == size:
                res.append(path[:])
                return

            for i in range(size):
                if not used[i]:
                    used[i] = True
                    path.append(nums[i])

                    dfs(nums, size, depth + 1, path, used, res)

                    used[i] = False
                    path.pop()

        size = len(nums)
        if len(nums) == 0:
            return []

        used = [False for _ in range(size)]
        res = []
        dfs(nums, size, 0, [], used, res)
        return res


if __name__ == '__main__':
    nums = [1, 1, 3]
    solution = Solution()
    res = solution.permute(nums)
    print(res)
