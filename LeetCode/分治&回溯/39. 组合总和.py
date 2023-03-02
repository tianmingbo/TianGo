# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 9:24
# @Author  : tmb
class Solution:
    def combinationSum(self, candidates, target: int):
        res = []

        def backtrack(candidates, res, path, target):
            # print(path)
            if target == 0:  # 终结条件
                res.append(path[:])
                return
            for i in range(len(candidates)):
                if target < 0:  # 剪枝
                    return
                # path.append(candidates[i])  # 选择
                # candidates[i:],过滤掉前一个元素，不再使用
                backtrack(candidates[i:], res, path + [candidates[i]], target - candidates[i])
                # path.pop()  # 撤销选择，恢复现场

        backtrack(candidates, res, [], target)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.combinationSum(candidates=[2, 3, 5], target=8))
