# -*- coding: utf-8 -*-
# @Time    : 2020/8/25 16:53
# @Author  : tmb
'''
491. 递增子序列

给定一个整型数组, 你的任务是找到所有该数组的递增子序列，递增子序列的长度至少是2。

示例:

输入: [4, 6, 7, 7]
输出: [[4, 6], [4, 7], [4, 6, 7], [4, 6, 7, 7], [6, 7], [6, 7, 7], [7,7], [4,7,7]]
'''


class Solution:
    def findSubsequences(self, nums):
        if not nums:
            return []
        res = set()  # 使用set去重
        res.add((nums[0],))
        for i in nums[1:]:
            res.update({j + (i,) for j in res if i >= j[-1]})
            res.add((i,))
        return [list(k) for k in res if len(k) > 1]  # 去掉长度为1的


class Solution2:
    def findSubsequences(self, nums):
        res = []

        def dfs(nums, tmp):
            if len(tmp) > 1:
                res.append(tmp)
            curPres = set()
            for inx, i in enumerate(nums):
                if i in curPres:
                    continue
                if not tmp or i >= tmp[-1]:
                    curPres.add(i)
                    dfs(nums[inx + 1:], tmp + [i])

        dfs(nums, [])
        return res


class Solution3:
    def findSubsequences(self, nums):
        res = []

        def dfs(nums, path):
            if len(path) > 1:
                res.append(path[:])
            for i in range(len(nums)):
                if not path or nums[i] >= path[-1]:
                    if i > 0 and nums[i] in nums[:i]:
                        continue
                    path.append(nums[i])
                    dfs(nums[i + 1:], path)
                    path.pop()

        dfs(nums, [])
        return len(res)


'''
[[4, 6], [4, 7], [4, 6, 7], [4, 6, 7, 7], [6, 7], [6, 7, 7], [7,7], [4,7,7]]
'''
if __name__ == '__main__':
    a = Solution3()
    print(a.findSubsequences([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 1, 1, 1, 1]))
