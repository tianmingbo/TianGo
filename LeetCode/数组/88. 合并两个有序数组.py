# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 11:28
# @Author  : tmb
from typing import List


class Solution:
    def merge(self, nums1, m: int, nums2, n: int) -> None:
        if not nums2:
            nums1 = nums1
        if not m:
            nums1[0:n] = nums2[0:n]
        num1_count = m - 1
        num2_count = n - 1
        all_count = m + n - 1
        while num1_count >= 0 and num2_count >= 0:  # 从大到小比较
            if nums1[num1_count] >= nums2[num2_count]:
                nums1[all_count] = nums1[num1_count]
                num1_count -= 1
            else:
                nums1[all_count] = nums2[num2_count]
                num2_count -= 1
            all_count -= 1
        nums1[0:num2_count + 1] = nums2[0:num2_count + 1]  # 未用完的nums2，添加到nums1的前面

    def merge2(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        p1, p2, p = m - 1, n - 1, (m + n) - 1
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] >= nums2[p2]:
                nums1[p] = nums1[p1]
                p -= 1
                p1 -= 1
            elif nums1[p1] < nums2[p2]:
                nums1[p] = nums2[p2]
                p -= 1
                p2 -= 1
        if p2 >= 0:
            nums1[:p2 + 1] = nums2[:p2 + 1]


if __name__ == '__main__':
    a = Solution()
    print(a.merge(nums1=[2, 0], m=1, nums2=[1], n=1))
