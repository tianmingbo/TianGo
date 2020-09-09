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

        def helper(index):
            if index == len(digits):
                res.append("".join(tmp))  # 不能append(tmp),浅拷贝，值会被覆盖
            else:
                digit = digits[index]
                for i in map[digit]:
                    tmp.append(i)
                    helper(index + 1)
                    tmp.pop()

        tmp = []  # 一轮遍历临时存储
        res = []  # 存储结果
        helper(0)
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
