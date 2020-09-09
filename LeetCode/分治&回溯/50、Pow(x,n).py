# -*- coding: utf-8 -*-
# @Time    : 2020/9/8 15:08
# @Author  : tmb
class Solution:
    def myPow(self, x: float, n: int) -> float:
        flag = False
        if n == 1:
            return x
        if n == 0:
            return 1.0
        if n < 0:
            flag = True
            n = -n
        res = self.myPow(x, n // 2)
        print(res)
        if n % 2 == 1:
            res = res * x * res
        else:
            res = res * res
        if flag:
            return 1 / res
        return res


class Solution2:
    def myPow(self, x: float, n: int) -> float:
        def quickMul(N):
            if N == 0:  # 退出条件
                return 1.0
            y = quickMul(N // 2)  # 递归到0
            print(y)
            return y * y if N % 2 == 0 else y * y * x

        return quickMul(n) if n >= 0 else 1.0 / quickMul(-n)


if __name__ == '__main__':
    a = Solution2()
    print(a.myPow(1.1, 111))
