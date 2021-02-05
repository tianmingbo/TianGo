# -*- coding: utf-8 -*-
# @Time    : 2020/9/9 16:07
# @Author  : tmb
class Solution:
    def letterCombinations(self, digits: str):
        if not digits:
            return []
        map = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz'
        }

        def backtrack(res, tmp, index):
            # 终结条件
            if len(tmp) == len(digits):
                res.append(''.join(tmp))
                return
            # 和全排列相比，更新nums
            digit = map[digits[index]]
            for i in digit:
                # 选择
                tmp.append(i)
                # 回溯
                backtrack(res, tmp, index + 1)
                # 撤销选择
                tmp.pop()

        res = []
        backtrack(res, [], 0)
        return res

    def letterCombinations2(self, digits):
        map = {'2': "abc", '3': "def", '4': "ghi", '5': "jkl", '6': "mno", '7': "pqrs",
               '8': "tuv", '9': "wxyz"}
        res = [''] if digits else []  # 为空返回[]
        for q in digits:
            res = [i + j for i in res for j in map[q]]  # niubility
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.letterCombinations2('23'))
