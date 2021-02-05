# -*- coding: utf-8 -*-
# @Time    : 2021/1/18 21:16
# @Author  : tmb
from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        tmp = [0 for _ in nums]
        for num in nums:
            if tmp[num - 1] == 1:  # 如果tmp[num - 1]==1，说明num已经出现过
                return num
            else:
                tmp[num - 1] = 1


if __name__ == '__main__':
    a = Solution()
    print(a.findDuplicate([1, 3, 4, 2, 2]))
