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


if __name__ == '__main__':
    a = Solution()
    print(a.maxSlidingWindow([9, 7, 6, 4, 3, 1], 3))
