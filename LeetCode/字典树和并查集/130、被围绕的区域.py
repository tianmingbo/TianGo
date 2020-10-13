# -*- coding: utf-8 -*-
# @Time    : 2020/10/9 14:53
# @Author  : tmb

class Solution1:
    # dfs
    def solve(self, board):
        if not board:
            return
        raw, col = len(board), len(board[0])

        def dfs(x, y):
            board[x][y] = 'L'
            for p, q in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if 0 <= p < raw and 0 <= q < col and board[p][q] == 'O':
                    dfs(p, q)

        '''
        思路：找到第一行（列），最后一行（列）相连的’O‘，把’O‘变成’L‘，然后再把里面的’O‘变’X‘
        '''
        for i in range(col):
            # 处理第一行,最后一行
            if board[0][i] == 'O':
                dfs(0, i)
            if board[raw - 1][i] == 'O':
                dfs(raw - 1, i)
        for j in range(raw):
            # 处理第一列，最后一列
            if board[j][0] == 'O':
                dfs(j, 0)
            if board[j][col - 1] == 'O':
                dfs(j, col - 1)
        for x in range(raw):
            for y in range(col):
                if board[x][y] == 'O':
                    board[x][y] = 'X'
                if board[x][y] == 'L':
                    board[x][y] = 'O'


class Solution2:
    # bfs
    def solve(self, board):
        if not board:
            return
        raw, col = len(board), len(board[0])

        def bfs(x, y):
            import collections
            queue = collections.deque()
            queue.append((x, y))
            while queue:
                i, j = queue.popleft()
                board[i][j] = 'L'
                for p, q in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:  # 遍历上下左右
                    if 0 <= p < raw and 0 <= q < col and board[p][q] == 'O':
                        queue.append((p, q))

        for i in range(col):
            # 处理第一行,最后一行
            if board[0][i] == 'O':
                bfs(0, i)
            if board[raw - 1][i] == 'O':
                bfs(raw - 1, i)
        for j in range(raw):
            # 处理第一列，最后一列
            if board[j][0] == 'O':
                bfs(j, 0)
            if board[j][col - 1] == 'O':
                bfs(j, col - 1)
        # 最后的处理
        for x in range(raw):
            for y in range(col):
                if board[x][y] == 'O':
                    board[x][y] = 'X'
                if board[x][y] == 'L':
                    board[x][y] = 'O'


class Solution3:
    # 并查集,没有看懂
    def solve(self, board) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        f = {}

        def find(x):
            f.setdefault(x, x)
            if f[x] != x:
                f[x] = find(f[x])
            return f[x]

        def union(x, y):
            f[find(y)] = find(x)

        if not board or not board[0]:
            return
        row = len(board)
        col = len(board[0])
        dummy = row * col
        for i in range(row):
            for j in range(col):
                if board[i][j] == "O":
                    if i == 0 or i == row - 1 or j == 0 or j == col - 1:
                        union(i * col + j, dummy)
                    else:
                        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            if board[i + x][j + y] == "O":
                                union(i * col + j, (i + x) * col + (j + y))
        for i in range(row):
            for j in range(col):
                if find(dummy) == find(i * col + j):
                    board[i][j] = "O"
                else:
                    board[i][j] = "X"


if __name__ == '__main__':
    a = Solution2()
    a.solve([["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"]]
            )
