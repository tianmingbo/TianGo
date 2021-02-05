# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 9:24
# @Author  : tmb
class Solution:
    def combinationSum(self, candidates, target: int):
        res = []

        def backtrack(candidates, res, tmp):
            if sum(tmp) == target:  # 终结条件
                res.append(tmp[:])
                return
            for i in range(len(candidates)):
                if sum(tmp) > target:  # 剪枝
                    break
                tmp.append(candidates[i])  # 选择
                backtrack(candidates[i:], res, tmp)  # candidates[i:],过滤掉前一个元素，不再使用
                tmp.pop()  # 撤销选择，恢复现场

        backtrack(candidates, res, [])
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.combinationSum(candidates=[2, 3, 5], target=8))
