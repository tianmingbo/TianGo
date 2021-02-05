# -*- coding: utf-8 -*-
# @Time    : 2021/1/9 17:19
# @Author  : tmb
from typing import List
import collections

'''
构建小顶堆
'''


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        res = []
        hash_tables = {}
        for i in nums:
            if i not in hash_tables:
                hash_tables[i] = 1
            else:
                hash_tables[i] += 1
        counts = list(hash_tables.values())  # 统计各个数字出现的次数
        self.heap_sort(counts)
        num_k = counts[:k]
        for j in num_k:
            for k, v in hash_tables.items():
                if v == j:
                    res.append(k)
                    hash_tables[k] = -1
        return res

    def build_min_heap(self, arr):
        # 构建最小堆
        n = len(arr)
        smallest = (n - 1) // 2
        for i in range(smallest, -1, -1):
            self.heapfy(arr, n, i)

    def heapfy(self, arr, length, parent):
        # 堆调整
        left = 2 * parent + 1
        right = 2 * parent + 2
        smallest = parent

        if left < length and arr[left] < arr[smallest]:
            smallest = left
        if right < length and arr[right] < arr[smallest]:  # 根左右。找到最小节点，交换值
            smallest = right

        if parent != smallest:
            arr[parent], arr[smallest] = arr[smallest], arr[parent]
            self.heapfy(arr, length, smallest)  # 递归调整

    def heap_sort(self, arr):
        # 堆排序
        self.build_min_heap(arr)
        n = len(arr)
        for i in range(n - 1, -1, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self.heapfy(arr, i, 0)

    def topKFrequent2(self, nums: List[int], k: int) -> List[int]:
        counter = collections.Counter(nums)
        return [i[0] for i in counter.most_common(k)]


if __name__ == '__main__':
    a = Solution()
    # a.heap_sort([2, 2, 3, 4, 2, 7, 9])
    #
    # print(a.arr)
    print(a.topKFrequent2(nums=[1, 2], k=2))
