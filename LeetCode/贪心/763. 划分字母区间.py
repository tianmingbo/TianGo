# -*- coding: utf-8 -*-
# @Time    : 2021/1/11 19:54
# @Author  : tmb
from typing import List


class Solution:
    def partitionLabels(self, S: str) -> List[int]:
        if not S:
            return []
        hash_alpha = [0] * 26
        for i in range(len(S)):  # 每个字母最后出现的位置
            hash_alpha[ord(S[i]) - ord('a')] = i
        left, right = 0, 0
        res = []
        for j in range(len(S)):
            right = max(right, hash_alpha[ord(S[j]) - ord('a')])  # 总是获取字母最后出现的index
            if j == right:  # 到了字母最后位置
                res.append(right - left + 1)
                left = j + 1
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.partitionLabels(S="ababcbacadefegdehijhklij"))
