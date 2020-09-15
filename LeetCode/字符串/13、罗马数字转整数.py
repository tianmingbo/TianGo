# -*- coding: utf-8 -*-
# @Time    : 2020/9/14 15:51
# @Author  : tmb
class Solution:
    def romanToInt(self, s: str) -> int:
        thousands = ["", "M", "MM", "MMM"]
        hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
        tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
        ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
        res=0
        tmp_str=''
        for i in s:
            tmp_str+=i
            if tmp_str not in map:
                continue
            else:
                pass



if __name__ == '__main__':
    a = Solution()
    a.romanToInt('MCMXCIV')
