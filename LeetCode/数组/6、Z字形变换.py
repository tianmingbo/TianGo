# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 15:32
# @Author  : tmb
'''
发现规律，周期 = 2 * numRows - 2 ，结合规律，把元素存在不同的数组中
'''
class Solution:
    def convert(self, s, numRows):
        if numRows == 1:
            return s
        res = [[] for i in range(numRows)]
        cycle = 2 * numRows - 2  # 规律
        for index, ch in enumerate(s):
            if index % cycle < numRows:
                res[index % cycle].append(ch)
            else:
                res[cycle - index % cycle].append(ch)
        tmp = [''.join(i) for i in res]
        return ''.join(tmp)


if __name__ == '__main__':
    a = Solution()
    print(a.convert("a", 1))
