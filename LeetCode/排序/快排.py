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


'''
递归，列表中取出第一个元素，作为标准，把比第一个元素小的都放在左侧，把比第一个元素大的都放在右侧，递归完成时就是排序结束的时候

时间复杂度O(nlogn)，空间复杂度O(logn)，不稳定
'''

if __name__ == '__main__':
    arr = [3, 1, 2, 9, 6, 4]
    n = len(arr)
    b = quick_sort(arr)
    print(b)
