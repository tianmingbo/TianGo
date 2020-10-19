# -*- coding: utf-8 -*-
# @Time    : 2020/10/19 10:44
# @Author  : tmb
class Sort:
    # 冒泡排序，两两比较，大的后移，O(n^2)时间复杂度，稳定排序
    def bubble_sort(li: list):
        for i in range(len(li) - 1):
            for j in range(i + 1, len(li)):
                if li[i] > li[j]:
                    li[i], li[j] = li[j], li[i]

    def select_sort(nums: list):
        # 选择排序，遍历一遍，找到最小的，然后继续遍历，O(n^2)时间复杂度，稳定排序
        for i in range(len(nums) - 1):
            min_index = i
            for j in range(i + 1, len(nums)):
                if nums[j] < nums[i]:
                    min_index = j
            nums[i], nums[min_index] = nums[min_index], nums[i]

    def insert_sort(nums: list):
        for i in range(len(nums)):
            current = nums[i]
            pre_index = i - 1
            while pre_index >= 0 and nums[pre_index] > current:
                nums[pre_index + 1] = nums[pre_index]
                pre_index -= 1
            nums[pre_index + 1] = current

    def shell_sort(nums: list):
        gap = len(nums) >> 1
        while gap > 0:
            for i in range(gap, len(nums)):
                current = nums[i]
                pre_index = i - gap
                while pre_index >= 0 and nums[pre_index] > current:
                    nums[pre_index + gap] = nums[pre_index]
                    pre_index -= gap
                nums[pre_index + gap] = current
            gap >>= 1
