# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 9:28
# @Author  : tmb

# 深度优先搜索，（递归）
class Solution:
    def generateParenthesis(self, n):
        if n == 0:
            return []
        res = []
        s = ''

        def _generate(left, right, s):
            '''
            :param left: 左括号已使用的个数
            :param right:  右括号已使用的个数
            :param s: 从根结点到叶子结点的路径字符串
            :return:
            '''
            if right == n and left == n:  # 终止条件，当左括号和右括号都用完了
                res.append(s)
                return
            if left < n:  # 如果左括号没有用完
                _generate(left + 1, right, s + '(')
            if right < left:  # 右括号已用的个数小于左括号
                _generate(left, right + 1, s + ')')

        _generate(0, 0, s)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.generateParenthesis(3))
