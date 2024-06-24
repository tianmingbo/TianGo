# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 11:26
# @Author  : tmb


class Solution:
    def cuttingRope(self, n: int) -> int:
        dp = [0 for _ in range(n + 1)]
        map = {2: 1, 3: 2, 4: 4, 5: 6, 6: 9}
        if n in map:
            return map[n]
        dp[2], dp[3], dp[4], dp[5], dp[6] = 1, 2, 4, 6, 9
        for i in range(7, n + 1):
            dp[i] = max(dp[i - 2] * 2, dp[i - 3] * 3)  # 从6往后，就可以找到规律
        return dp[n] % (10 ** 9 + 7)


'''

给你一根长度为 n 的绳子，请把绳子剪成整数长度的 m 段（m、n都是整数，n>1并且m>1），每段绳子的长度记为 k[0],k[1]...k[m-1] 。请问 k[0]*k[1]*...*k[m-1] 可能的最大乘积是多少？例如，当绳子的长度是8时，
我们把它剪成长度分别为2、3、3的三段，此时得到的最大乘积是18。

'''
if __name__ == '__main__':
    a = Solution()
    print(a.cuttingRope(1000))
