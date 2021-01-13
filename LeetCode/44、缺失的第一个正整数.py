'''
my：找到一个最大值，for i……max ：if i not i nums
return i
时间复杂度O(2n),空间O(1)
index时间复杂度为O(1)
in为O(n)
'''


class Solution:
    def firstMissingPositive(self, nums):
        max_num = -1
        for i in nums:
            if i > max_num:
                max_num = i
        if max_num < 0:
            return 0
        for j in range(1, len(nums) + 1):
            try:
                nums.index(j)
            except:
                return j
        return max_num + 1


if __name__ == '__main__':
    a = Solution()
    print(a.firstMissingPositive([2, 3]))
