# -*- coding: utf-8 -*-
# @Time    : 2020/9/9 17:22
# @Author  : tmb
class Solution:
    def solveNQueens(self, n: int):
        def generateBoard():
            board = list()
            for i in range(n):
                row[queens[i]] = "Q"
                board.append("".join(row))
                row[queens[i]] = "."
            return board

        def backtrack(row: int):
            if row == n:
                board = generateBoard()
                print(board)
                solutions.append(board)
            else:
                for i in range(n):
                    if i in columns or row - i in diagonal1 or row + i in diagonal2:
                        continue
                    queens[row] = i
                    print(queens)
                    columns.add(i)
                    diagonal1.add(row - i)
                    diagonal2.add(row + i)
                    backtrack(row + 1)
                    columns.remove(i)
                    diagonal1.remove(row - i)
                    diagonal2.remove(row + i)

        solutions = list()
        queens = [-1] * n
        columns = set()
        diagonal1 = set()
        diagonal2 = set()
        row = ["."] * n
        backtrack(0)
        return solutions


class Solution2:
    def solveNQueens(self, n: int):
        def generate_board(queens):
            tmp = [['.' for _ in range(n)] for _ in range(n)]
            for i in range(len(tmp)):
                tmp[i][queens[i]] = 'Q'
                tmp[i] = ''.join(tmp[i])
            res.append(tmp)

        def helper(raw):
            if raw == n:
                generate_board(queens)  # 走到最后一层，说明是一种有效解法.按照要求生成结果
            else:
                for i in range(n):
                    if i in columns or raw - i in xy_diff or raw + i in xy_add:  # 左斜对角线|右斜对角线|同一列。判断冲突
                        continue
                    queens[raw] = i  # 所在位置
                    xy_diff.add(raw - i)  # 左斜
                    xy_add.add(raw + i)  # 右斜
                    columns.add(i)  # 同一列已使用
                    helper(raw + 1)
                    columns.remove(i)
                    xy_add.remove(raw + i)
                    xy_diff.remove(raw - i)

        res = []
        xy_diff = set()  # 左斜对角线
        xy_add = set()  # 右斜对角线
        queens = [-1] * n
        columns = set()  # 列
        helper(0)
        return res


if __name__ == '__main__':
    a = Solution()
    a.solveNQueens(4)
    # print(a.solveNQueens(3))
