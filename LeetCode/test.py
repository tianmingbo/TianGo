class Solution:
    def solveNQueens(self, n: int):
        def generate_board(queens):
            tmp = [['.' for _ in range(n)] for _ in range(n)]
            for i in range(len(tmp)):
                tmp[i][queens[i]] = 'Q'
                tmp[i] = ''.join(tmp[i])
            res.append(tmp)

        def helper(raw):
            if raw == n:
                generate_board(queens)  # 走到最后一层，说明是一种有效解法
            else:
                for i in range(n):
                    if i in columns or raw - i in xy_diff or raw + i in xy_add:  # 左斜对角线|右斜对角线|同一列。判断冲突
                        continue
                    queens[raw] = i  # 同一列已使用
                    xy_diff.add(raw - i)
                    xy_add.add(raw + i)
                    columns.add(i)
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
    print(a.solveNQueens(5))
