# -*- coding: utf-8 -*-
# @Time    : 2020/9/11 20:36
# @Author  : tmb

class Solution2:
    # 深度优先搜索，把每一块岛屿变成‘0’水
    def numIslands(self, grid) -> int:
        count = 0
        max_raw, max_col = len(grid), len(grid[0])

        def dfs(raw, col):
            grid[raw][col] = 0  # floodfill算法，赋值为0，已被洪水淹没
            for x, y in [(raw + 1, col), (raw - 1, col), (raw, col + 1), (raw, col - 1)]:  # 遍历上下左右
                if 0 <= x < max_raw and 0 <= y < max_col and grid[x][y] == '1':
                    dfs(x, y)

        for i in range(max_raw):
            for j in range(max_col):
                if grid[i][j] == '1':
                    count += 1  # 如果是1，就把相关联的1，全变成0，岛屿数量加1
                    dfs(i, j)
        return count


class Solution3:
    # 广度优先
    def numIslands(self, grid) -> int:
        if not grid:
            return 0
        count = 0
        import collections
        queue = collections.deque()
        max_raw, max_col = len(grid), len(grid[0])  # 最大行，最大列
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '1':
                    queue.append((i, j))
                    count += 1
                    while queue:  # 如果当前岛屿四周存在岛屿，就入栈，变为0
                        raw, col = queue.popleft()
                        grid[raw][col] = '0'
                        for x, y in [(raw + 1, col), (raw - 1, col), (raw, col + 1), (raw, col - 1)]:
                            if 0 <= x < max_raw and 0 <= y < max_col and grid[x][y] == '1':
                                queue.append((x, y))
        return count


class Solution:
    def dfs(self, grid, r, c):
        grid[r][c] = 0
        nraw, ncol = len(grid), len(grid[0])
        for x, y in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if 0 <= x < nraw and 0 <= y < ncol and grid[x][y] == "1":
                self.dfs(grid, x, y)

    def numIslands(self, grid) -> int:
        nraw = len(grid)
        if nraw == 0:
            return 0
        ncol = len(grid[0])

        num_islands = 0
        for r in range(nraw):
            for c in range(ncol):
                if grid[r][c] == "1":
                    num_islands += 1
                    self.dfs(grid, r, c)

        return num_islands


if __name__ == '__main__':
    a = Solution2()
    print(a.numIslands([
        ['1', '1', '1', '1', '0'],
        ['1', '1', '0', '1', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '0', '0', '1']
    ]
    ))
