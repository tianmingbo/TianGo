# -*- coding: utf-8 -*-
# @Time    : 2020/10/19 10:54
# @Author  : tmb
def merge_sort(nums: list):
    if len(nums) <= 1:  # 递归退出条件
        return nums
    mid = len(nums) >> 1
    left = merge_sort(nums[:mid])  # 拆分子问题
    right = merge_sort(nums[mid:])

    def merge(left, right):  # 合并两个有序数组
        res = []
        l, r = 0, 0
        while l < len(left) and r < len(right):
            if left[l] <= right[r]:
                res.append(left[l])
                l += 1
            else:
                res.append(right[r])
                r += 1
        res += left[l:]
        res += right[r:]
        print(res)
        return res

    return merge(left, right)


'''
分治算法，拆分成子序列，使用归并排序，将排序好的子序列合并成一个最终的排序序列。关键在于怎么合并：设定两个指针，最初位置分别为两个已经排序序列的起始位置，
比较两个指针所指向的元素，选择相对小的元素放到合并空间，并将该指针移到下一位置，直到某一指针超出序列尾，将另一序列所剩下的所有元素直接复制到合并序列尾。

时间复杂度$O(nlogn)$，空间复杂度O(n)，不稳定
'''

if __name__ == '__main__':
    nums = [89, 3, 3, 2, 5, 45, 33, 67]  # [2, 3, 3, 5, 33, 45, 67, 89]
    c = merge_sort(nums)
    print(c)
