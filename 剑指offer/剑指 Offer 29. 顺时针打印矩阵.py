from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix:
            return []
        left, right, top, bottom = 0, len(matrix[0]) - 1, 0, len(matrix) - 1
        res = []
        counter = len(matrix) * len(matrix[0])
        while counter >= 1:
            for i in range(left, right + 1):
                if counter>=1:
                    res.append(matrix[top][i])
                    counter -= 1
            top += 1

            for j in range(top, bottom + 1):
                if counter >= 1:
                    res.append(matrix[j][right])
                    counter -= 1
            right -= 1

            for k in range(right, left - 1, -1):
                if counter >= 1:
                    res.append(matrix[bottom][k])
                    counter -= 1
            bottom -= 1

            for z in range(bottom, top - 1, -1):
                if counter >= 1:
                    res.append(matrix[z][left])
                    counter -= 1
            left += 1
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.spiralOrder(matrix=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))
