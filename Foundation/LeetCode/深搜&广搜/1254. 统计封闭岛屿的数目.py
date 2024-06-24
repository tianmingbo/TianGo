#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author bo~
    @Date 2023/3/2 18:31
    @Describe  同200岛屿问题，只是需要先把周边处理
"""
from typing import List


class Solution:
    def closedIsland(self, grid: List[List[int]]) -> int:
        counter = 0
        max_raw, max_col = len(grid), len(grid[0])

        def dfs(raw, col):
            if grid[raw][col] == 1:
                return
            grid[raw][col] = 1
            for x, y in [(raw + 1, col), (raw - 1, col), (raw, col + 1), (raw, col - 1)]:
                if 0 <= x < max_raw and 0 <= y < max_col and grid[x][y] == 0:
                    dfs(x, y)

        # 先把四周淹没
        for i in range(max_raw):
            dfs(i, 0)
            dfs(i, max_col - 1)
        for j in range(max_col):
            dfs(0, j)
            dfs(max_raw - 1, j)

        for i in range(max_raw):
            for j in range(max_col):
                if grid[i][j] == 0:
                    dfs(i, j)
                    counter += 1
        return counter
