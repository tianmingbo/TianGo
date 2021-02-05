# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 17:27
# @Author  : tmb
class Solution:
    def isHappy(self, n: int) -> bool:
        appeared = set()
        while True:
            sum_num = self.get_num(n)
            if sum_num == 1:
                return True
            else:
                # sum_num出现过，说明进入了循环
                if sum_num in appeared:
                    return False
                else:
                    appeared.add(sum_num)
            n = sum_num

    def get_num(self, n):
        sum_num = []
        while n:
            sum_num.append(n % 10)
            n //= 10
        sum_num = sum([i ** 2 for i in sum_num])
        return sum_num


if __name__ == '__main__':
    a = Solution()
    print(a.isHappy(19))
