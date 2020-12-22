# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 20:49
# @Author  : tmb
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # 注意浅拷贝问题,超时
        if not s or not p:
            return []
        tmp = {}
        for i in p:
            if i not in tmp:
                tmp[i] = 1
            else:
                tmp[i] += 1
        tmp2 = tmp.copy()
        ele_index = 0
        res = []
        while ele_index < len(s):
            tmp = tmp2.copy()
            for j in range(ele_index, len(s)):
                if j - ele_index >= len(p):
                    break
                if s[j] in tmp:
                    if tmp[s[j]]:
                        tmp[s[j]] -= 1
                    if tmp[s[j]] == 0:
                        tmp.pop(s[j])
                    if not tmp:
                        res.append(ele_index)
            ele_index += 1
        return res

    def findAnagrams2(self, s: str, p: str) -> List[int]:
        # 使用滑动窗口
        res = []
        start_index = 0
        while start_index < (len(s) - len(p) + 1):
            for i in range(start_index, len(s) - len(p) + 1):
                flag = self.isEctopicword(s[i:i+len(p)], p)
                if flag:
                    res.append(i)
                start_index += 1
                break
        return res

    def isEctopicword(self, s, p):
        tmp1, tmp2 = {}, {}
        for i in s:
            if i in tmp1:
                tmp1[i] += 1
            else:
                tmp1[i] = 1
        for j in p:
            if j in tmp2:
                tmp2[j] += 1
            else:
                tmp2[j] = 1
        return tmp1 == tmp2


if __name__ == '__main__':
    a = Solution()
    print(a.findAnagrams2(s="baaaaaaaaaaaaa", p="aa"))
