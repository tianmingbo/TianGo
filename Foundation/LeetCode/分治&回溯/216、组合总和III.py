# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 11:01
# @Author  : tmb
from typing import List


class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:

        possible_num = [i + 1 for i in range(9)]
        res = []

        def backtrack(nums, path, n):

            if len(path) == k and n == 0:  # 终止条件
                res.append(path[:])
                return
            if len(path) > k or n < 0:  # 剪枝
                return
            for i in range(len(nums)):
                path.append(nums[i])
                backtrack(nums[i + 1:], path, n - nums[i])
                path.pop()

        backtrack(possible_num, [], n)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.combinationSum3(2, 6))
