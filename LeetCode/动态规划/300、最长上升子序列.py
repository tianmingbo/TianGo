# -*- coding: utf-8 -*-
# @Time    : 2020/9/1 11:42
# @Author  : tmb

'''
我的思路： 1、遍历
2、动态规划，向前寻找比当前小的那个位置，统计那个位置前面比自己小的个数  dp[i]=max(dp[j])+1

'''


class Solution:
    def lengthOfLIS(self, nums):
        if not nums:
            return 0
        tmp = []
        dp = [1 for _ in nums]
        for i in range(1, len(nums)):
            for j in range(i, -1, -1):
                if nums[j] < nums[i]:  # 统计前方所有比当前位置小的元素
                    tmp.append(dp[j])
            if tmp:
                dp[i] += max(tmp)  # 取最大值
            tmp = []
        print(dp)
        return max(dp)


# 贪心+二分
class Solution2:
    def lengthOfLIS(self, nums):
        d = []
        for n in nums:
            if not d or n > d[-1]:
                d.append(n)
            else:
                l, r = 0, len(d) - 1
                loc = r
                while l <= r:
                    mid = (l + r) // 2
                    if d[mid] >= n:
                        loc = mid
                        r = mid - 1
                    else:
                        l = mid + 1
                d[loc] = n
        return len(d)


if __name__ == '__main__':
    a = Solution()
    print(a.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]))
