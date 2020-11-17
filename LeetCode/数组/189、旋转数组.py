# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 13:42
# @Author  : tmb

# 空间复杂度要求O(1)
class Solution:
    def rotate(self, nums, k):
        if not nums:
            return
        k = k % len(nums)
        tmp = nums[::-1]
        res = tmp[:k][::-1] + tmp[k:][::-1]
        return res

    #     self.nums = nums
    #     n = len(nums)
    #     k = k % n
    #     self.reverse(0, n - k - 1)
    #     self.reverse(n - k, n - 1)
    #     self.reverse(0, n - 1)
    #
    # def reverse(self, l, r):
    #     while l < r:
    #         self.nums[l], self.nums[r] = self.nums[r], self.nums[l]
    #         l += 1
    #         r -= 1


'''
1 2 3 4 5 6 7->翻转
7 6 5 4 3 2 1->翻转前k个
5 6 7 4 3 2 1->翻转后n-k个
5 6 7 1 2 3 4
'''

if __name__ == '__main__':
    a = Solution()
    print(a.rotate([1, 2, 3, 4, 5, 6, 7], 3))
