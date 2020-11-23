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

        def backtrack(candidates, res, tmp):
            if sum(tmp) == target and tmp not in res:  # 终结条件,不能包含重复解
                res.append(tmp[:])
                return
            for i in range(len(candidates)):
                if sum(tmp) > target:  # 剪枝
                    break
                tmp.append(candidates[i])  # 选择
                backtrack(candidates[i + 1:], res, tmp)  # candidates[i:],过滤掉前一个元素，不再使用
                tmp.pop()  # 撤销选择，恢复现场

        backtrack(candidates, res, [])
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
    print(a.combinationSum(candidates=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           target=27))
