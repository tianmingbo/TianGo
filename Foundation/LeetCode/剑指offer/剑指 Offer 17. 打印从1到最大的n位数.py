# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 18:17
# @Author  : tmb
from typing import List


class Solution:
    def printNumbers(self, n: int) -> List[int]:
        return list(range(1, 10 ** n))


if __name__ == '__main__':
    a = Solution()
    print(a.printNumbers(3))
