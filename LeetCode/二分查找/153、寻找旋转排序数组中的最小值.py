# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 17:34
# @Author  : tmb
class Solution(object):
    def findMin(self, nums):
        if len(nums) == 1:
            return nums[0]

        left = 0
        # right pointer
        right = len(nums) - 1

        if nums[right] > nums[0]:
            return nums[0]
        while right >= left:
            mid = left + (right - left) // 2
            if nums[mid] > nums[mid + 1]:
                return nums[mid + 1]
            if nums[mid - 1] > nums[mid]:
                return nums[mid]
            if nums[mid] > nums[0]:
                left = mid + 1
            else:
                right = mid - 1


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
