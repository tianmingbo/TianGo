# 双端队列
from collections import deque


class Solution:
    def maxSlidingWindow(self, nums, k: int):
        if len(nums) * k == 0:
            return []
        tmp = max(nums[:k])
        res_deque = []
        for i in range(len(nums) - k):
            res_deque.append((tmp))
            if nums[k + i] > tmp:
                tmp = nums[i + k]
            else:
                if nums[i] == tmp:
                    tmp = max(nums[i + 1:i + k + 1])
        res_deque.append(tmp)
        return res_deque

    def maxSlidingWindow2(self, nums, k):
        win, ret = [], []
        for i, v in enumerate(nums):
            if i >= k and win[0] <= i - k:
                win.pop(0)
            while win and nums[win[-1]] <= v:
                win.pop()
            win.append(i)
            if i >= k - 1:
                ret.append(nums[win[0]])
        return ret


if __name__ == '__main__':
    a = Solution()
    print(a.maxSlidingWindow2([9, 10, 6, 4, 3, 1], 3))
