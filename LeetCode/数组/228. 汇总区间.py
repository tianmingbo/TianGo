# -*- coding: utf-8 -*-
# @Time    : 2021/1/10 14:59
# @Author  : tmb
from typing import List


class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        if not nums:
            return []
        if len(nums) == 1:
            return [str(nums[0])]
        i, j = 0, 1
        res = []
        while j < len(nums):
            if nums[j] - nums[j - 1] > 1:
                if j - i == 1:
                    res.append(str(nums[i]))
                    i += 1
                else:
                    res.append(str(nums[i]) + '->' + str(nums[j - 1]))
                    i = j
                j += 1
            else:
                j += 1
        # 做最后的处理
        if j - i == 1:
            res.append(str(nums[i]))
        else:
            res.append(str(nums[i]) + '->' + str(nums[j - 1]))
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.summaryRanges([0, 1, 2, 3, 4, 7]))
