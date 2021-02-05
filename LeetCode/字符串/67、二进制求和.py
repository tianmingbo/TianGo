# -*- coding: utf-8 -*-
# @Time    : 2020/9/9 17:38
# @Author  : tmb
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        tmp = list(str(int(a) + int(b)))
        for i in range(len(tmp) - 1, 0, -1):
            if int(tmp[i]) >= 2:
                tmp[i - 1] = str(int(tmp[i - 1]) + 1)
                tmp[i] = str(int(tmp[i]) - 2)
        if int(tmp[0]) >= 2:
            tmp[0] = str(int(tmp[0]) - 2)
            tmp.insert(0, '1')
        return ''.join(tmp)

class Solution2:
    def addBinary(self, a, b) -> str:
        # x, y = int(a, 2), int(b, 2)
        # while y:
        #     answer = x ^ y
        #     carry = (x & y) << 1
        #     x, y = answer, carry
        # return bin(x)[2:]
        return bin(int(a,2)+int(b,2))[2:]

if __name__ == '__main__':
    a = Solution2()
    print(a.addBinary('1111', '1111'))
