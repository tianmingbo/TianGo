from typing import List


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        self.flag = False  # 是否找到可行解

        def dfs(depth):
            if depth == len(spaces):
                self.flag = True
                return
            i, j = spaces[depth]
            for digit in range(9):
                if not raw[i][digit] and not col[digit][j] and not block[i // 3][j // 3][digit]:  # 是否可以添加
                    raw[i][digit] = True  # 选择
                    col[digit][j] = True
                    block[i // 3][j // 3][digit] = True
                    board[i][j] = str(digit + 1)
                    dfs(depth + 1)  # 回溯
                    raw[i][digit] = False  # 撤销选择
                    col[digit][j] = False
                    block[i // 3][j // 3][digit] = False
                if self.flag:
                    return

        raw = [[False] * 9 for _ in range(9)]  # 记录每行使用的
        col = [[False] * 9 for _ in range(9)]  # 每列使用过的
        block = [[[False] * 9 for _ in range(3)] for _ in range(3)]  # 3*3的小方块
        spaces = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    spaces.append((i, j))  # 记录有多少个没有添加，最大深度
                else:
                    digit = int(board[i][j]) - 1
                    raw[i][digit] = True
                    col[digit][j] = True
                    block[i // 3][j // 3][digit] = True
        dfs(0)
        print(board)


if __name__ == '__main__':
    a = Solution()
    a.solveSudoku([["5", "3", ".", ".", "7", ".", ".", ".", "."],
                   ["6", ".", ".", "1", "9", "5", ".", ".", "."],
                   [".", "9", "8", ".", ".", ".", ".", "6", "."],

                   ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
                   ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
                   ["7", ".", ".", ".", "2", ".", ".", ".", "6"],

                   [".", "6", ".", ".", ".", ".", "2", "8", "."],
                   [".", ".", ".", "4", "1", "9", ".", ".", "5"],
                   [".", ".", ".", ".", "8", ".", ".", "7", "9"]])
