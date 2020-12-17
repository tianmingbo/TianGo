from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums:
            return 0
        dp = [0 for _ in range(len(nums))]
        dp[0] = 1
        count = 0
        for i in range(1, len(nums)):
            for j in range(i + 1):
                if nums[j] <= nums[i]:
                    count += 1
            dp[i] = max(dp[i - 1], count)
            count = 0
        return max(dp)


if __name__ == '__main__':
    a = Solution()
    print(a.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]))
