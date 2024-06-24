# -*- coding: utf-8 -*-
# @Time    : 2020/9/9 15:40
# @Author  : tmb


'''
思路：1、排序，nums[n/2]就是多数元素，时间复杂度O(nlogn)
2、哈希，
3、分治：没有看懂
'''


class Solution:
    def majorityElement(self, nums) -> int:
        nums.sort()
        return nums[len(nums) // 2]


class Solution2:
    def majorityElement(self, nums, lo=0, hi=None):
        def majority_element_rec(lo, hi):
            # base case; the only element in an array of size 1 is the majority
            # element.
            if lo == hi:
                return nums[lo]

            # recurse on left and right halves of this slice.
            mid = (hi - lo) // 2 + lo
            left = majority_element_rec(lo, mid)
            right = majority_element_rec(mid + 1, hi)

            # if the two halves agree on the majority element, return it.
            if left == right:
                return left

            # otherwise, count each element and return the "winner".
            left_count = sum(1 for i in range(lo, hi + 1) if nums[i] == left)
            right_count = sum(1 for i in range(lo, hi + 1) if nums[i] == right)

            return left if left_count > right_count else right

        return majority_element_rec(0, len(nums) - 1)


if __name__ == '__main__':
    a = Solution2()
    print(a.majorityElement([2, 1, 1, 1, 1, 2, 2]))
