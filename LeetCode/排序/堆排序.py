# -*- coding: utf-8 -*-
# @Time    : 2020/10/19 10:54
# @Author  : tmb
def heap_sort(nums: list):
    def heapify(parent_index, length, nums):
        temp = nums[parent_index]  # 根节点的值
        chile_index = 2 * parent_index + 1  # 左节点，再加一为右节点
        while chile_index < length:
            if chile_index + 1 < length and nums[chile_index + 1] > nums[chile_index]:
                chile_index = chile_index + 1
            if temp > nums[chile_index]:
                break
            nums[parent_index] = nums[chile_index]  # 使得根节点最大
            parent_index = chile_index
            chile_index = 2 * parent_index + 1
        nums[parent_index] = temp

    for i in range((len(nums) - 2) >> 1, -1, -1):
        heapify(i, len(nums), nums)  # 1.建立大根堆
        print(nums)
    for j in range(len(nums) - 1, 0, -1):
        nums[j], nums[0] = nums[0], nums[j]
        heapify(0, j, nums)  # 2.堆排序，为升序


'''
思想：根节点最大，大顶堆，对应升序，根节点最小，小顶堆。

构建大根堆，完全二叉树结构，初始无序
最大堆调整，进行堆排序。将堆顶元素与最后一个元素交换，此时后面有序
时间复杂度$O(nlogn)$，原地排序，稳定
'''
if __name__ == '__main__':
    nums = [89, 3, 3, 2, 5, 45, 33, 67]  # [2, 3, 3, 5, 33, 45, 67, 89]
    heap_sort(nums)
    print(nums)
