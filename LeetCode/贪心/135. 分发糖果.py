# -*- coding: utf-8 -*-
# @Time    : 2021/1/10 18:35
# @Author  : tmb
from typing import List

'''
遇到两个维度权衡的时候，一定要先确定一个维度，再确定另一个维度。
'''


class Solution:
    def candy(self, ratings: List[int]) -> int:
        if not ratings:
            return 0
        candy = [1] * len(ratings)  # 基础保证每人一个

        # 从左往右，大于前面的那个，+1
        for i in range(1, len(ratings)):
            if ratings[i] > ratings[i - 1]:
                candy[i] = candy[i - 1] + 1

        # 从右往左，小于前面的，已经加过糖的，不需要再加
        for j in range(len(ratings) - 2, -1, -1):
            if ratings[j] > ratings[j + 1]:
                candy[j] = max(candy[j], candy[j + 1] + 1)
        # print(candy)
        return sum(candy)


if __name__ == '__main__':
    a = Solution()
    print(a.candy([1, 2, 87, 87, 87, 2, 1]))
