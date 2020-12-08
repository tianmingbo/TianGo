# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 16:35
# @Author  : tmb
from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        seen_once = seen_twice = 0

        for num in nums:
            # first appearance:
            # add num to seen_once
            # don't add to seen_twice because of presence in seen_once

            # second appearance:
            # remove num from seen_once
            # add num to seen_twice

            # third appearance:
            # don't add to seen_once because of presence in seen_twice
            # remove num from seen_twice
            seen_once = ~seen_twice & (seen_once ^ num)
            seen_twice = ~seen_once & (seen_twice ^ num)

        return seen_once


if __name__ == '__main__':
    a = Solution()
    print(a.singleNumber([0, 1, 0, 1, 0, 1, 99]))
