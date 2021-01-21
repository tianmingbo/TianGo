# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 15:07
# @Author  : tmb

# 时间复杂度O(n^2)
class Solution:
    def threeSum(self, nums):
        if len(nums) <= 2:
            return []
        nums.sort()  # O(nlogn)
        res = []
        for k in range(len(nums) - 1):  # O(n^2)
            if k > 0 and nums[k] == nums[k - 1]:  # 取出重复使用的元素
                continue
            i = k + 1
            j = len(nums) - 1
            while i < j:
                s = nums[k] + nums[i] + nums[j]
                if s == 0:
                    res.append([nums[k], nums[i], nums[j]])
                    # 去除重复元素
                    while i < j and nums[i] == nums[i + 1]:
                        i += 1
                    while i < j and nums[j] == nums[j - 1]:
                        j -= 1
                    i += 1
                    j -= 1
                elif s > 0:
                    j -= 1
                else:
                    i += 1
        return res


'''
使用暴力解法，时间复杂度O(n^3)
解题思路；
首先排序，然后选定一个元素，使用双指针，当三元素相加时，如果大于0，说明右指针大了，-1，同理，左指针也是。
使用set去重,时间复杂度为O(n^2)
'''

if __name__ == '__main__':
    a = Solution()
    print(a.threeSum([-2, 0, 0, 2, 2]))
