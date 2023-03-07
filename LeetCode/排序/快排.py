# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 9:23
# @Author  : tmb

def quick_sort(li: list):
    if li == []:
        return []
    first = li[0]
    # 推导式实现
    left = quick_sort([l for l in li[1:] if l < first])
    right = quick_sort([r for r in li[1:] if r >= first])
    return left + [first] + right


def quick_sort2(begin, end, nums):
    if begin >= end:
        return
    pivot_index = partition(begin, end, nums)
    quick_sort2(begin, pivot_index - 1, nums)
    quick_sort2(pivot_index + 1, end, nums)


def partition(begin, end, nums):
    pivot = nums[begin]  # 初始化一个待比较数据
    mark = begin
    for i in range(begin + 1, end + 1):
        if nums[i] < pivot:
            mark += 1
            nums[mark], nums[i] = nums[i], nums[mark]
    nums[begin], nums[mark] = nums[mark], nums[begin]
    return mark


def quick_select(nums, k, begin, end):
    """
    将快速排序改成快速选择，即我们希望寻找到一个位置，这个位置左边是k个比这个位置上的数更小的数，
    右边是n-k-1个比该位置上的数大的数，找到这个位置后停止迭代，完成了一次划分。

    """
    if begin >= end:
        return
    pivot_index = partition(begin, end, nums)
    if pivot_index == k:
        return
    elif pivot_index < k:
        quick_select(nums, k, pivot_index + 1, end)
    else:
        quick_select(nums, k, begin, pivot_index - 1)


# 获得前k小的数
def topk_smalls(nums, k):
    quick_select(nums, k, 0, len(nums) - 1)
    return nums[:k]


# 获得第k小的数
def topk_small(nums, k):
    quick_select(nums, k, 0, len(nums) - 1)
    return nums[k - 1]


# 获得前k大的数
def topk_larges(nums, k):
    # partition是按从小到大划分的，如果让index左边为前n-k个小的数，则index右边为前k个大的数
    quick_select(nums, len(nums) - k, 0, len(nums) - 1)  # 把k换成len(nums)-k
    return nums[len(nums) - k:]


# 获得第k大的数
def topk_large(nums, k):
    # partition是按从小到大划分的，如果让index左边为前n-k个小的数，则index右边为前k个大的数
    quick_select(nums, len(nums) - k, 0, len(nums) - 1)  # 把k换成len(nums)-k
    return nums[len(nums) - k]


'''
递归，列表中取出第一个元素，作为标准，把比第一个元素小的都放在左侧，把比第一个元素大的都放在右侧，递归完成时就是排序结束的时候

时间复杂度O(nlogn)，空间复杂度O(logn)，不稳定
'''

if __name__ == '__main__':
    # arr = [4, 5, 8, 3, 2]
    # n = len(arr)
    # quick_sort2(0, 4, arr)
    # print('res', arr)
    arr = [1, 3, 2, 3, 0, -19]
    k = 3
    print(topk_small(arr, k))
    print(arr)
