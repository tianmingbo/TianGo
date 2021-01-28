# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 21:15
# @Author  : tmb
# -*- coding:utf-8 -*-

class Solution:
    '''
    快排排序，返回第n-K个
    '''

    def findKth(self, a, n, K):
        self.quick_sort(a, 0, n - 1, K)
        return a[n - K]

    def quick_sort(self, arr, begin, end, K):
        if begin >= end:
            return
        pivot_index = self.partition(arr, begin, end)
        self.quick_sort(arr, begin, pivot_index - 1, K)
        self.quick_sort(arr, pivot_index + 1, end, K)

    def partition(self, arr, begin, end):
        prepare = arr[begin]
        mark = begin
        for i in range(begin + 1, end + 1):
            if arr[i] < prepare:
                mark += 1
                arr[mark], arr[i] = arr[i], arr[mark]
        arr[mark], arr[begin] = arr[begin], arr[mark]
        return mark


'''
未理解2
'''


def findKth2(a, start, end, K):
    low, high = start, end
    key = a[start]
    while start < end:
        while start < end and a[end] <= key:
            end -= 1
        a[start] = a[end]
        while start < end and a[start] >= key:
            start += 1
        a[end] = a[start]
    a[start] = key
    if start < K - 1:
        return findKth2(a, start + 1, high, K)
    elif start > K - 1:
        return findKth2(a, low, start - 1, K)
    else:
        return a[start]


if __name__ == '__main__':
    a = Solution()
    print(a.findKth(
        [1332802, 1177178, 1514891, 871248, 753214, 123866, 1615405, 328656, 1540395, 968891, 1884022, 252932, 1034406,
         1455178, 821713, 486232, 860175, 1896237, 852300, 566715, 1285209, 1845742, 883142, 259266, 520911, 1844960,
         218188, 1528217, 332380, 261485, 1111670, 16920, 1249664, 1199799, 1959818, 1546744, 1904944, 51047, 1176397,
         190970, 48715, 349690, 673887, 1648782, 1010556, 1165786, 937247, 986578, 798663], 49, 24))
