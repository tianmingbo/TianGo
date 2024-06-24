# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 18:21
# @Author  : tmb
class Solution:
    def translateNum(self, num: int) -> int:
        str_num = str(num)
        dp = [0 for _ in range(len(str_num) + 1)]
        dp[0] = 1
        dp[1] = 1
        for i in range(2, len(str_num) + 1):
            if 10 <= int(str_num[i - 2:i]) <= 25:
                dp[i] = dp[i - 1] + dp[i - 2]
            else:
                dp[i] = dp[i - 1]
        return dp[len(str_num)]


'''
1225:
1 2 2 5
12 2 5
1 22 5
1 2 25
12 25
'''
if __name__ == '__main__':
    a = Solution()
    print(a.translateNum(506))
