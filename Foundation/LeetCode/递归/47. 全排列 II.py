# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 17:33
# @Author  : tmb
from typing import List


class Solution:

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
                # path.append(_nums[i])
                backtrack(_nums[:i] + _nums[i + 1:], path+[_nums[i]])
                # path.pop()

        backtrack(sorted(nums), [])
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.permuteUnique2([1, 5, 1, 1, 1]))
