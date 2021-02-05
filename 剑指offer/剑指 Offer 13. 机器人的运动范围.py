# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 22:18
# @Author  : tmb
class Solution:
    def movingCount(self, m: int, n: int, k: int) -> int:
        '''
        :param m:行
        :param n: 列
        :param k: 行+列  各个位数之和
        :return:  符合条件的个数
        使用广度优先
        '''
        if not k:
            return 1
        res = set()
        queue = [(0, 0)]
        while queue:
            x, y = queue.pop(0)
            if (x, y) not in res and 0 <= x < m and 0 <= y < n and self.digitsum(x) + self.digitsum(y) <= k:
                res.add((x, y))
                for nx, ny in [(x + 1, y), (x, y + 1)]:
                    queue.append((nx, ny))

        return len(res)

    def digitsum(self, num):
        sum = 0
        while num > 9:
            sum += num % 10
            num //= 10
        sum += num
        return sum


if __name__ == '__main__':
    a = Solution()
    print(a.movingCount(m=11, n=8, k=16))
