# -*- coding: utf-8 -*-
# @Time    : 2020/9/8 16:15
# @Author  : tmb

'''
https://leetcode-cn.com/problems/subsets/solution/hui-su-suan-fa-by-powcai-5/
md，好菜啊，我不会，别人却能给出三种，炸裂
'''
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


class Solution:
    def subsets(self, nums):
        res = [[]]
        for i in nums:
            res = res + [[i] + j for j in res]
        return res


class Solution2:
    def subsets(self, nums):
        res = []
        n = len(nums)

        def helper(i, tmp):
            res.append(tmp)
            for j in range(i, n):
                helper(j + 1, tmp + [nums[j]])

        helper(0, [])
        return res


# https://leetcode-cn.com/problems/subsets/solution/hui-su-si-xiang-tuan-mie-pai-lie-zu-he-zi-ji-wen-t/

class Solution3(object):
    def subsets(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        def DFS(nums, s, index):
            # 终止条件
            if len(nums) == index:
                res.append(s)
                return
            DFS(nums, s + [nums[index]], index + 1)  # 选取当前元素
            DFS(nums, s, index + 1)  # 不选取当前元素

        res = []
        s = []
        DFS(nums, s, 0)
        return res


'''
my
'''


class Solution5(object):
    def subsets(self, nums):
        res = []

        def backtrack(tmp, nums, index):
            res.append(tmp[:])
            for i in range(index, len(nums)):
                # 做选择
                tmp.append(nums[i])
                # 回溯
                backtrack(tmp, nums, i + 1)
                # 撤销选择
                tmp.pop()

        backtrack([], nums, 0)
        return res


class Solution4(object):
    def subsets(self, nums):
        def backtrack(nums, tmp, index):
            if len(nums) == index:  # 选或不选，已有元素已经选完
                res.append(tmp)
                return
            backtrack(nums, tmp + [nums[index]], index + 1)  # 选取当前元素
            backtrack(nums, tmp, index + 1)  # 不选当前元素

        res = []
        tmp = []
        backtrack(nums, tmp, 0)
        return res


if __name__ == '__main__':
    a = Solution5()
    print(a.subsets([1, 2, 3]))
