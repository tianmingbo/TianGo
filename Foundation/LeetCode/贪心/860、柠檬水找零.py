# -*- coding: utf-8 -*-
# @Time    : 2020/9/12 10:08
# @Author  : tmb
# 贪心
class Solution:
    def lemonadeChange(self, bills) -> bool:
        five, ten = 0, 0
        for i in bills:
            if i == 5:
                five += 1
            elif i == 10:
                if not five:
                    return False
                five -= 1
                ten += 1
            else:
                if five and ten:  # 优先找10
                    ten -= 1
                    five -= 1
                else:
                    five -= 3
                if ten < 0 or five < 0:
                    return False
        return True


if __name__ == '__main__':
    a = Solution()
    print(a.lemonadeChange([5, 5, 5, 10, 20]))
