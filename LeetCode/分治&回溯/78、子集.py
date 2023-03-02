# -*- coding: utf-8 -*-
# @Time    : 2020/9/8 16:15
# @Author  : tmb

'''
result = []
def backtrack(路径, 选择列表):
    if 满足结束条件:
        result.add(路径)
        return
    for 选择 in 选择列表:
        做选择
        backtrack(路径, 选择列表)
        撤销选择

'''


class Solution(object):
    def subsets(self, nums):
        res = []

        def backtrack(path, nums):
            res.append(path[:])
            for i in range(len(nums)):
                # 做选择
                path.append(nums[i])
                # 回溯
                backtrack(path, nums[i + 1:])
                # 撤销选择
                path.pop()

        backtrack([], nums)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.subsets([1, 2, 3]))
