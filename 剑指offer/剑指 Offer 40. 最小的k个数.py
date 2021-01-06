# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 20:08
# @Author  : tmb
from typing import List


class Solution:
    def build_heap(self, arr):
        n = len(arr)
        last_parent = (n - 1) // 2
        for i in range(last_parent, -1, -1):
            self.heapfy(arr, n, i)

    def heapfy(self, arr, length, parent):
        left = 2 * parent + 1
        right = 2 * parent + 2
        largest = parent

        if left < length and arr[left] > arr[largest]:
            largest = left
        if right < length and arr[right] > arr[largest]:
            largest = right

        if largest != parent:
            arr[parent], arr[largest] = arr[largest], arr[parent]
            self.heapfy(arr, length, largest)

    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        # 堆
        self.build_heap(arr)
        n = len(arr)
        for i in range(n - 1, -1, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self.heapfy(arr, i, 0)
        return arr[:k]


if __name__ == '__main__':
    a = Solution()
    print(a.getLeastNumbers(arr=[3, 2, 1, 4], k=2))
