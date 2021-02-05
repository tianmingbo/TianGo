# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 17:33
# @Author  : tmb
from typing import List


class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        if not nums:
            return []
        res = []
        used = []

        def backtrack(nums, tmp, used):
            # 终结条件
            if len(tmp) == len(nums):
                if tmp[:] not in res:
                    res.append(tmp[:])
                return
            for i in range(len(nums)):
                # 选择
                if i in used:
                    continue
                used.append(i)
                tmp.append(nums[i])
                # 回溯
                backtrack(nums, tmp, used)
                # 撤销选择
                tmp.pop()
                used.pop()

        backtrack(nums, [], used)
        return res

    def permuteUnique2(self, nums: List[int]) -> List[List[int]]:
        if not nums:
            return []
        res = []
        n = len(nums)

        def backtrack(_nums, path):
            if len(path) == n:
                res.append(path[:])
                return
            for i in range(len(_nums)):
                if i > 0 and _nums[i] == _nums[i - 1]:
                    continue
                path.append(_nums[i])
                backtrack(_nums[:i] + _nums[i + 1:], path)
                path.pop()

        backtrack(sorted(nums), [])
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.permuteUnique2([1, 5, 1]))
