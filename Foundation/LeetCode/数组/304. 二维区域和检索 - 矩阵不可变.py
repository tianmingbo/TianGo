from typing import List


# 前缀和

class NumMatrix:
    pre_sum = []

    def __init__(self, matrix: List[List[int]]):
        self.pre_sum = [[0 for _ in range(len(matrix[0]) + 1)] for _ in range(len(matrix) + 1)]
        for i in range(1, len(matrix) + 1):
            for j in range(1, len(matrix[0]) + 1):
                self.pre_sum[i][j] = self.pre_sum[i - 1][j] + self.pre_sum[i][j - 1] + matrix[i - 1][j - 1] - \
                                     self.pre_sum[i - 1][j - 1]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return self.pre_sum[row2 + 1][col2 + 1] - self.pre_sum[row1][col2 + 1] - self.pre_sum[row2 + 1][col1] + \
               self.pre_sum[row1][col1]


if __name__ == '__main__':
    num = NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]])
    print(num.sumRegion(1, 2, 2, 4))
