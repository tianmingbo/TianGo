# -*- coding: utf-8 -*-
# @Time    : 2020/11/6 21:33
# @Author  : tmb
class Solution:
    def reverseWords(self, s: str) -> str:
        left, right = 0, len(s) - 1
        # 去掉两边的空格
        while left < right and s[left] == ' ':
            left += 1
        while left < right and s[right] == ' ':
            right -= 1
        import collections
        deque, tmp = collections.deque(), []
        while left <= right:
            if s[left] == ' ' and tmp:  # 遇到空格的时候，就添加到队列中
                deque.appendleft(''.join(tmp))  # 压入左边
                tmp = []
            elif s[left] != ' ':
                tmp.append(s[left])
            left += 1
        deque.appendleft(''.join(tmp))  # 处理最后一个单词
        return ' '.join(deque)


if __name__ == '__main__':
    a = Solution()
    print(a.reverseWords('example   good a'))
