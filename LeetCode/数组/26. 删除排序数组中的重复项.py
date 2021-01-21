# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 10:59
# @Author  : tmb
class Solution:
    def removeDuplicates(self, nums) -> int:
        if not nums:
            return 0
        i = 0
        for j in range(1, len(nums)):
            if nums[i] != nums[j]:
                i += 1
                nums[i] = nums[j]
        return i + 1


# 使用双指针

if __name__ == '__main__':
    a = Solution()
    print(a.removeDuplicates([1, 1, 2, 2, 3, 3]))
