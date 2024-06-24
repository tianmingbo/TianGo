# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 21:28
# @Author  : tmb
from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        if not board:
            return False
        self.flag = False

        def backtrack(visited, i, j, depth):
            if depth == len(word):
                self.flag = True
                return
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and (i, j) not in visited and board[i][j] == word[
                depth] and not self.flag:
                visited.append((i, j))
                backtrack(visited, i + 1, j, depth + 1)
                backtrack(visited, i - 1, j, depth + 1)
                backtrack(visited, i, j + 1, depth + 1)
                backtrack(visited, i, j - 1, depth + 1)
                visited.pop()

        for i in range(len(board)):
            for j in range(len(board[0])):
                visited = []
                if self.flag:
                    return True
                backtrack(visited, i, j, 0)
        return self.flag


class Solution2:
    def exist(self, board: List[List[str]], word: str) -> bool:
        if not (len(board) and len(board[0])):
            return False
        m, n = len(board), len(board[0])
        lw = len(word)
        if m * n < len(word):
            return False
        dp = [[True] * n for _ in range(m)]
        res = False

        def dfs(i, j, cur, res):
            if res:
                return res
            if dp[i][j] and board[i][j] == word[cur]:
                if cur == lw - 1:
                    return True
                dp[i][j] = False
                if i < m - 1:
                    res |= dfs(i + 1, j, cur + 1, res)
                if i > 0:
                    res |= dfs(i - 1, j, cur + 1, res)
                if j < n - 1:
                    res |= dfs(i, j + 1, cur + 1, res)
                if j > 0:
                    res |= dfs(i, j - 1, cur + 1, res)
                dp[i][j] = True
            else:
                return False
            return res

        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0]:
                    res |= dfs(i, j, 0, res)
                    if res:
                        break
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.exist([["C", "A", "A"], ["A", "A", "A"], ["B", "C", "D"]], "AAB"))
