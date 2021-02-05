# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 17:34
# @Author  : tmb
class Solution(object):
    def findMin(self, nums):
        if len(nums) == 1:
            return nums[0]
        left, right = 0, len(nums) - 1
        while left <= right:
            if nums[left] <= nums[right]:  # 当left<right时，说明是递增的，直接返回left的值
                return nums[left]
            mid = (left + right) // 2
            if nums[left] <= nums[mid]:  # 如果nums[left] <= nums[mid]，说明left到mid是递增的，最小值不在这之间。要到left+1~right中查找
                left = mid + 1
            else:
                right = mid  # 如果nums[left] > nums[mid]，说明left到mid不是递增的，最小值在这之间。在left~right中查找（注意right不-1，因为mid没有被排除）
        return -1


if __name__ == '__main__':
    a = Solution()
    print(a.findMin([3, 4, 5, 1, 2]))

'''
public int findMin(int[] nums) {
    int left = 0, right = nums.length - 1;
    while (left < right) {
        int middle = (left + right) / 2;
        if (nums[middle] < nums[right]) {
            // middle可能是最小值
            right = middle;
        } else {
            // middle肯定不是最小值
            left = middle + 1;
        }
    }
    return nums[left];
}
'''
