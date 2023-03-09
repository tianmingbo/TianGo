# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 19:18
# @Author  : tmb
from typing import List


class Solution:
    def permutation(self, s: str) -> List[str]:
        if len(s) == 1:
            return [s]
        n = len(s)
        all_elem = sorted([i for i in s])
        res = []

        def backtrack(elem, path):
            if len(path) == n:  # 终结条件
                res.append(''.join(path[:]))
                return
            for j in range(len(elem)):
                if j > 0 and elem[j] == elem[j - 1]:  # 过滤掉重复元素
                    continue
                path.append(elem[j])
                backtrack(elem[:j] + elem[j + 1:], path)  # 除了当前元素，剩下的可挑选的元素
                path.pop()

        backtrack(all_elem, [])
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.permutation('aca'))
