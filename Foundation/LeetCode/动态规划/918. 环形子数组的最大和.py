from typing import List


class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        ans, n = 0, len(nums)
        max_sum, min_sum = nums[0], nums[0]
        cur_max, cur_min = 0, 0
        for i in range(n):
            cur_max = max(cur_max + nums[i], nums[i])
            max_sum = max(max_sum, cur_max)  # 最大子序和
            cur_min = min(cur_min + nums[i], nums[i])
            min_sum = min(min_sum, cur_min)  # 最小子序和
            print(min_sum)
            ans += nums[i]  # 数组和
        print(ans)
        return max(max_sum, ans - min_sum) if max_sum > 0 else max_sum  # ans - （-min_sum）  =ans+min_sum 加上循环过程中损失的数值


if __name__ == '__main__':
    solution = Solution()
    # 总和-8，循环过程中损失了-21，必然有个子序列的和等于13
    print(solution.maxSubarraySumCircular([9, -4, -5, -4, -5, -3, 4]))
