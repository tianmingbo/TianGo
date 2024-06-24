# -*- coding: utf-8 -*-
# @Time    : 2020/11/22 15:30
# @Author  : tmb


class Solution(object):
    def exist(self, board, word):
        raw, col = len(board), len(board[0])
        self.found = False  # 标志位，有没有匹配

        def dfs(raw, col, length, visited):
            if length == len(word):  # 回溯终止条件
                self.found = True
                return
            if not self.found and 0 <= raw < len(board) and 0 <= col < len(board[0]) and (raw, col) not in visited and \
                    board[raw][col] == word[length]:  # 条件过滤，确保当前没有访问过且 board[raw][col] == word[length]，满足这个条件才继续向下回溯
                visited.append((raw, col))  # 选择
                dfs(raw + 1, col, length + 1, visited)  # 上下左右回溯
                dfs(raw - 1, col, length + 1, visited)
                dfs(raw, col + 1, length + 1, visited)
                dfs(raw, col - 1, length + 1, visited)
                visited.pop()  # 撤销选择

        for i in range(raw):
            for j in range(col):
                visited = []  # 记录已访问过
                if self.found == True:  # 如果匹配到，提前结束
                    return True
                dfs(i, j, 0, visited)
        return self.found


if __name__ == '__main__':
    a = Solution()
    print(a.exist(board=
    [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ], word='ABCCED'))
