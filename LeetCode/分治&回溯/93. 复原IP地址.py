# -*- coding: utf-8 -*-
# @Time    : 2020/11/22 16:51
# @Author  : tmb
from typing import List


class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        if len(s) <= 3 or len(s) > 12:  # ip长度大于3，小于13
            return []
        res = []

        def backtrack(_s, path, depth):
            if not _s and depth == 4 and path not in res:  # ip分四段
                if self.isvalid(path):
                    res.append(path[:])
                    return
            if depth > 4:  # 超过4段，不合格
                return
            for i in range(1, 4):  # 判断每位ip,是否符合规则
                if _s and 0 <= int(_s[:i]) <= 255:
                    path.append(_s[:i])  # 选择
                else:
                    continue
                backtrack(_s[i:], path, depth + 1)  # ip有四段
                path.pop()  # 撤销选择

        backtrack(s, [], 0)
        return ['.'.join(i) for i in res]

    def isvalid(self, path):
        """
        判断ip是不是大于1，且0开头的
        :param path:
        :return: bool
        """
        for i in path:
            if len(i) > 1 and i[0] == '0':
                return False
        return True


if __name__ == '__main__':
    a = Solution()
    print(a.restoreIpAddresses('25525511135'))
