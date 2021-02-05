# -*- coding: utf-8 -*-
# @Time    : 2020/9/18 17:59
# @Author  : tmb
def countAndSay( n: int) -> str:
    res = '1'
    for _ in range(n-1):  # 控制循环次数
        i, tmp = 0, ''
        for j, c in enumerate(res):
            if c != res[i]:
                tmp += str(j-i) + res[i]
                i = j
        res = tmp + str(len(res) - i) + res[-1]
    return res

if __name__ == '__main__':
    print(countAndSay(20))