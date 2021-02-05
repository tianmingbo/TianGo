# -*- coding: utf-8 -*-
# @Time    : 2021/2/2 20:26
# @Author  : tmb
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # 经典bfs
        if not grid:
            return 0
        queue = []
        for a in range(len(grid)):
            for b in range(len(grid[0])):
                if grid[a][b] == 2:  # 烂橘子可能不止一个
                    queue.append((a, b))
        count = 0
        visited = set()  # 已经访问过的
        while queue:
            count += 1  # 需要蔓延的次数
            for _ in range(len(queue)):
                x, y = queue.pop(0)
                grid[x][y] = 2  # 橘子变坏
                for new_x, new_y in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]:  # 上下左右
                    if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] == 1 and (
                            new_x, new_y) not in visited:
                        queue.append((new_x, new_y))
                        visited.add((new_x, new_y))
        for x in range(len(grid)):  # 看看还有没有好橘子
            for y in range(len(grid[0])):
                if grid[x][y] == 1:
                    return -1
        return count - 1 if count else 0


if __name__ == '__main__':
    b = Solution()
    print(b.orangesRotting([[0]]))
