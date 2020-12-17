# -*- coding: utf-8 -*-
# @Time    : 2020/10/20 17:06
# @Author  : tmb
'''
func reversePairs(nums []int) int {
	// 归并排序
	return mergeSort(nums, 0, len(nums)-1)
}
func mergeSort(arr []int, l int, r int) int {
	if l >= r {
		return 0
	}
	count, mid := 0, (l+r)>>1
	count = mergeSort_(arr, l, mid) + mergeSort_(arr, mid+1, r) // 1
	temp, i, k := make([]int, r-l+1), l, 0
	for j, idx := mid+1, l; j <= r; j++ { // 2
		for ; i <= mid && arr[i] < arr[j]; i++ {
			temp[k], k = arr[i], k+1 // 2.1
		}
		temp[k], k = arr[j], k+1                      // 2.2
		for idx <= mid && (arr[idx]+1)>>1 <= arr[j] { // 3
			idx++ // 3.1
		}
		count += mid - idx + 1 // 3.2
	}
	copy(arr[l+k:], arr[i:mid+1]) // 2.3
	copy(arr[l:], temp[:k])       // 4
	return count
}

'''


class Solution:
    def reversePairs(self, nums):
        return self.mergeSort(nums, 0, len(nums) - 1)

    def mergeSort(self, nums, start, end):
        if start >= end:
            return 0
        mid = (start + end) // 2 + 1
        count = self.mergeSort(nums, start, mid - 1) + self.mergeSort(nums, mid, end)
        j = mid
        for i in range(start, mid):
            while j <= end and nums[j] * 2 < nums[i]:
                j += 1
            count += (j - mid)
        nums[start:end + 1] = sorted(nums[start:end + 1])
        return count


class Solution2:
    def reversePairs(self, nums):
        return self.mergeSort(nums, 0, len(nums) - 1)

    def mergeSort(self, nums, start, end):
        if start >= end:
            return 0
        mid = (start + end) // 2 + 1
        # print(mid)
        count = self.mergeSort(nums, start, mid - 1) + self.mergeSort(nums, mid, end)
        j = mid
        for i in range(start, mid):
            while j <= end and nums[j] * 2 < nums[i]:
                j += 1
            count += (j - mid)
        nums[start:end + 1] = sorted(nums[start:end + 1])
        return count


if __name__ == '__main__':
    a = Solution2()
    print(a.reversePairs([2, 4, 3, 5, 1]))
