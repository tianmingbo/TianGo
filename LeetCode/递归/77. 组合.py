# -*- coding: utf-8 -*-
# @Time    : 2020/11/18 9:09
# @Author  : tmb

class Solution(object):
    def combine(self, n, k):
        ret = []
        self.dfs(list(range(1, n + 1)), k, [], ret)
        return ret

    def dfs(self, nums, k, path, ret):
        if len(path) == k:
            ret.append(path)
            return
        for i in range(len(nums)):
            self.dfs(nums[i + 1:], k, path + [nums[i]], ret)


class Solution2:
    def combine(self, n: int, k: int):
        result = []

        def recall(num, start, path):
            if len(path) == k:
                result.append(path[:])
                return
            for i in range(start, num + 1):
                path.append(i)
                recall(num, i + 1, path)
                path.pop()

        recall(n, 1, [])
        return result


'''
实质是树的遍历
'''


class Solution3(object):
    def combine(self, n, k):
        if not k:
            return []
        res = []

        def backtrace(nums, tmp, res, k):
            # 终止条件
            if len(tmp) == k:
                res.append(tmp[:])
                return
            for i in range(len(nums)):
                # 选择
                tmp.append(nums[i])
                # 回溯
                backtrace(nums[i + 1:], tmp, res, k)  # 假如选了1，剩下的就只有2,3,4可选
                # 撤销选择
                tmp.pop()

        backtrace(list(range(1, n + 1)), [], res, k)
        return res


if __name__ == '__main__':
    a = Solution3()
    print(a.combine(3, 3))
