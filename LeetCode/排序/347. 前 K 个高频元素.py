# -*- coding: utf-8 -*-
# @Time    : 2021/1/9 17:19
# @Author  : tmb
from typing import List

'''
构建小顶堆
'''


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        hash_tables = {}
        for i in nums:
            if i not in hash_tables:
                hash_tables[i] = 1
            else:
                hash_tables[i] += 1
        counts = list(hash_tables.values())
        print(counts)

    def build_min_heap(self, arr):
        self.arr = arr
        n = len(self.arr)
        min_parent = (n - 1) // 2
        for i in range(min_parent, -1, -1):
            self.heapfy(self.arr, n, i)

    def heapfy(self, arr, length, parent):
        left = 2 * parent + 1
        right = 2 * parent + 2
        smallest = parent

        if left < length and arr[left] < arr[parent]:
            smallest = left
        if right < length and arr[right] < arr[parent]:
            smallest = right

        if parent != smallest:
            self.arr[parent], self.arr[smallest] = self.arr[smallest], self.arr[parent]
            self.heapfy(self.arr, length, smallest)

    def heap_sort(self, arr):
        self.build_min_heap(arr)
        n = len(self.arr)
        for i in range(n - 1, -1, -1):
            self.arr[i], self.arr[0] = self.arr[0], self.arr[i]
            self.heapfy(self.arr, i, 0)


if __name__ == '__main__':
    a = Solution()
    a.heap_sort([2, 2, 3, 4, 2, 7, 9])

    print(a.arr)
    # print(a.topKFrequent(nums=[1, 1, 1, 2, 2, 3], k=2))
