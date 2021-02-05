# -*- coding: utf-8 -*-
# @Time    : 2021/1/8 20:52
# @Author  : tmb
class Solution:
    def maximumSwap(self, num: int) -> int:
        nums = [int(i) for i in str(num)]
        max_num = -1
        tmp = [0 for _ in range(len(nums))]
        for i in range(len(nums) - 1, -1, -1):
            if nums[i] > max_num:
                tmp[i] = i
                max_num = nums[i]
            else:
                tmp[i] = tmp[i + 1]

        for j in range(len(nums)):
            if tmp[j] == j or nums[j] == nums[tmp[j]]:  # 防止1993提前交换
                continue
            nums[j], nums[tmp[j]] = nums[tmp[j]], nums[j]
            break
        nums = [str(i) for i in nums]
        return int(''.join(nums))


if __name__ == '__main__':
    a = Solution()
    print(a.maximumSwap(1993))
