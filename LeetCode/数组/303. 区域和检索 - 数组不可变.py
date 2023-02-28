from typing import List


# 前缀和

class NumArray:
    pre_sum = []  # preSum[i]记录nums[0..i-1]的累加和

    def __init__(self, nums: List[int]):
        self.pre_sum = [0 for _ in range(len(nums) + 1)]
        for i in range(1, len(self.pre_sum)):
            self.pre_sum[i] = self.pre_sum[i - 1] + nums[i - 1]

    def sumRange(self, left: int, right: int) -> int:
        return self.pre_sum[right + 1] - self.pre_sum[left]  # O(1)


if __name__ == '__main__':
    arr = NumArray([-2, 0, 3, -5, 2, -1])
    print(arr.sumRange(0, 2))
