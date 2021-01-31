from typing import List

'''
利用快排思想，部分排序
'''


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        n = len(nums)
        start, end = 0, n - 1
        pivot = -1
        while pivot != n - k:
            print(nums)
            if pivot < n - k:
                start, pivot, t = self.partition(nums, pivot + 1, end)
            else:
                start, pivot, t = self.partition(nums, start, pivot - 1)
        return nums[pivot]

    def partition(self, nums, start, end):
        pilot = start
        l = start + 1
        r = end
        while l <= r:
            if nums[l] > nums[pilot]:
                nums[l], nums[r] = nums[r], nums[l]
                r -= 1
            else:
                l += 1
        nums[pilot], nums[r] = nums[r], nums[pilot]
        return start, r, end


if __name__ == '__main__':
    a = Solution()
    print(a.findKthLargest([3, 2, 1, 5, 6, 4], 2))
