# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 19:21
# @Author  : tmb
class Solution:
    def monotoneIncreasingDigits(self, N: int) -> int:
        repeat_count = 0
        tmp = list(str(N))
        for i in range(len(tmp) - 1):
            if tmp[i + 1] < tmp[i]:
                tmp[i - repeat_count] = str(int(tmp[i - repeat_count]) - 1)
                for j in range(i + 1 - repeat_count, len(tmp)):
                    tmp[j] = '9'
            if tmp[i + 1] == tmp[i]:  # 记录重复数字
                repeat_count += 1
            else:
                repeat_count = 0
        return int(''.join(tmp))

    def monotoneIncreasingDigits2(self, N: int) -> int:
        # 从后向前
        sn = list(str(N))
        n = len(sn)
        if n == 1:
            return N
        for i in range(n - 1, 0, -1):
            if sn[i - 1] <= sn[i]:
                continue
            else:
                # 如果当前元素小于前一个元素
                sn[i - 1] = str(int(sn[i - 1]) - 1)
                for j in range(i, n):
                    sn[j] = str(9)

        return int(''.join(sn))


'''
总体思路就是先找到第一个小于上一个值的index，然后把前一个值减一，最后把index后面的变成9。注意重复数字
'''
if __name__ == '__main__':
    a = Solution()
    print(a.monotoneIncreasingDigits2(332))
