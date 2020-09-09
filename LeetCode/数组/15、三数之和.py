# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 15:07
# @Author  : tmb

'''
使用暴力解法，时间复杂度O(n^3)
解题思路；
首先排序，然后选定一个元素，使用双指针，当三元素相加时，如果大于0，说明右指针大了，-1，同理，左指针也是。
使用set去重
'''


# 时间复杂度O(n^2)
class Solution:
    def threeSum(self, nums):
        if len(nums) <= 2:
            return []
        nums.sort()  # O(nlogn)
        res = set()
        for k in range(len(nums) - 1):  # O(n^2)
            i = k + 1
            j = len(nums) - 1
            while i < j:
                if nums[k] + nums[i] + nums[j] == 0:
                    res.update({(nums[k], nums[i], nums[j])})
                    i += 1
                    j -= 1
                elif nums[k] + nums[i] + nums[j] > 0:
                    j -= 1
                else:
                    i += 1
        return [list(i) for i in res]
        # if len(nums) <= 2:
        #     return []
        # res = []
        # nums = sorted(nums)
        # if nums[0] > 0 or nums[-1] < 0:
        #     return []
        #
        # for i in range(len(nums)):
        #     if (i > 0 and nums[i] == nums[i - 1]):
        #         continue
        #     j = i + 1
        #     k = len(nums) - 1
        #     while j < k:
        #         if nums[i] + nums[j] + nums[k] == 0:
        #             while (j < k and nums[j] == nums[j + 1]):
        #                 j += 1
        #             while (k > j and nums[k] == nums[k - 1]):
        #                 k -= 1
        #             res.append([nums[i], nums[j], nums[k]])
        #             j += 1
        #             k -= 1
        #         elif nums[i] + nums[j] + nums[k] > 0:
        #             k -= 1
        #         else:
        #             j += 1
        #
        # return res


if __name__ == '__main__':
    a = Solution()
    print(a.threeSum([3, 0, -2, -1, 1, 2]))
