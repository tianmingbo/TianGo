# -*- coding: utf-8 -*-
# @Time    : 2020/11/22 16:31
# @Author  : tmb
from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        if not nums:
            return []
        res = []
        nums.sort()  # 首先需要排序，如[4, 4, 4, 1, 4]，不排序会出错

        def backtrack(nums, path):
            res.append(path[:])
            for i in range(len(nums)):
                if i > 0 and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                backtrack(nums[i + 1:], path)  # 回溯，1,已选择，只能在后面的[2,2]中选择
                path.pop()

        backtrack(nums, [])
        return res


class Solution2(object):
    def subsetsWithDup(self, nums):
        ret = []
        self.dfs(sorted(nums), [], ret)
        return ret

    def dfs(self, nums, path, ret):
        ret.append(path)
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            self.dfs(nums[i + 1:], path + [nums[i]], ret)


if __name__ == '__main__':
    a = Solution()
    print(a.subsetsWithDup([1, 2, 2]))
