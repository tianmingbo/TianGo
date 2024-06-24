# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 19:50
# @Author  : tmb
import time


class Solution:
    def nthUglyNumber(self, n: int) -> int:
        ugly = {1, 2, 3, 4, 5}
        l_ugly = [1, 2, 3, 4, 5]
        if n < len(l_ugly):
            return l_ugly[n - 1]
        num, count = 6, 6
        before = time.time()
        while count <= n:
            if num / 2 in ugly or num / 3 in ugly or num / 5 in ugly:
                ugly.add(num)
                l_ugly.append(num)
                count += 1
            num += 1
        print(time.time() - before)
        return l_ugly[n - 1]


class Ugly:
    def __init__(self):
        before = time.time()
        self.nums = nums = [1, ]
        i2 = i3 = i5 = 0

        for i in range(1, 1690):
            ugly = min(nums[i2] * 2, nums[i3] * 3, nums[i5] * 5)
            nums.append(ugly)

            if ugly == nums[i2] * 2:
                i2 += 1
            if ugly == nums[i3] * 3:
                i3 += 1
            if ugly == nums[i5] * 5:
                i5 += 1
        print(time.time() - before)


class Solution2:
    u = Ugly()

    def nthUglyNumber(self, n):
        return self.u.nums[n - 1]


if __name__ == '__main__':
    a = Solution()
    print(a.nthUglyNumber(453))
