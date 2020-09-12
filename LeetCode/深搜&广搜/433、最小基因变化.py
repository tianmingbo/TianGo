# -*- coding: utf-8 -*-
# @Time    : 2020/9/11 15:51
# @Author  : tmb
class Solution:
    def minMutation(self, start: str, end: str, bank) -> int:
        possible = ["A", "C", "G", "T"]
        queue = [(start, 0)]
        while queue:
            # 广度优先遍历模板
            word, step = queue.pop(0)
            if word == end:
                return step
            for i in range(len(word)):
                for p in possible:
                    # 从第0个位置开始匹配新的字符串
                    temp = word[:i] + p + word[i + 1:]
                    # 在bank里面就处理(set中in操作复杂度是0(1))
                    if temp in bank:
                        # 从bank里移除，避免重复计数
                        bank.remove(temp)
                        # 加入队列，步数加1
                        queue.append((temp, step + 1))
        return -1


if __name__ == '__main__':
    a = Solution()
    print(a.minMutation("AACCGGTT", "AAACGGTA", ["AACCGGTA", "AACCGCTA", "AAACGGTA"]))
