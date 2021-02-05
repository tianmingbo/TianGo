# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 16:50
# @Author  : tmb

class Solution:
    def myAtoi(self, str: str) -> int:
        if not str:
            return 0
        str = str.strip()
        import re
        res = re.findall('^[\+\-]?\d+', str)
        print(res)
        if not res:
            return 0
        res = int(res[0])
        if res > 2 ** 31 - 1:
            return 2 ** 31 - 1
        if res < -2 ** 31:
            return -2 ** 31
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.myAtoi('-231234.434'))
