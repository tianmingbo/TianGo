from typing import List


class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        neighbors = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        rows = len(board)
        cols = len(board[0])

        # 遍历面板每一个格子里的细胞
        for row in range(rows):
            for col in range(cols):
                # 对于每一个细胞统计其八个相邻位置里的活细胞数量
                live_neighbors = 0
                for neighbor in neighbors:
                    # 相邻位置的坐标
                    r = (row + neighbor[0])
                    c = (col + neighbor[1])
                    # 查看相邻的细胞是否是活细胞
                    if (r < rows and r >= 0) and (c < cols and c >= 0) and abs(board[r][c]) == 1:
                        live_neighbors += 1
                # 规则 1 或规则 3
                if board[row][col] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                    # -1 代表这个细胞过去是活的现在死了
                    board[row][col] = -1
                # 规则 4
                if board[row][col] == 0 and live_neighbors == 3:
                    # 2 代表这个细胞过去是死的现在活了
                    board[row][col] = 2
        # 遍历 board 得到一次更新后的状态
        for row in range(rows):
            for col in range(cols):
                if board[row][col] > 0:
                    board[row][col] = 1
                else:
                    board[row][col] = 0
        print(board)


if __name__ == '__main__':
    a = Solution()
    print(a.gameOfLife(board=[[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]))
