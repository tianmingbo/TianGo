# -*- coding: utf-8 -*-
# @Time    : 2020/11/22 18:17
# @Author  : tmb
from typing import List


class Solution:
    def combinationSum(self, candidates, target: int):
        if sum(candidates) < target:
            return []
        res = []
        candidates.sort()

        def backtrack(candidates, path, target):
            if target == 0:  # 终结条件,不能包含重复解
                res.append(path[:])
                return
            if target < 0:
                return
            for i in range(len(candidates)):
                if i > 0 and candidates[i] == candidates[i - 1]:  # 重复数字不使用
                    continue
                path.append(candidates[i])  # 选择
                backtrack(candidates[i + 1:], path, target - candidates[i])  # candidates[i:],过滤掉前一个元素，不再使用
                path.pop()  # 撤销选择，恢复现场

        backtrack(candidates, [], target)
        return res

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        def dfs(begin, path, residue):
            if residue == 0:
                res.append(path[:])
                return

            for index in range(begin, size):
                if candidates[index] > residue:
                    break

                if index > begin and candidates[index - 1] == candidates[index]:
                    continue

                path.append(candidates[index])
                dfs(index + 1, path, residue - candidates[index])
                path.pop()

        size = len(candidates)
        if size == 0:
            return []

        candidates.sort()
        res = []
        dfs(0, [], target)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.combinationSum([10, 1, 2, 7, 6, 1, 5], 8))
