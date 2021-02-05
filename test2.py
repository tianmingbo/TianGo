class Solution:
    def rotateMatrix(self, mat, n):
        if not mat:
            return []
        res = []
        for j in range(n):
            tmp = []
            for i in range(n):
                tmp.append(mat[i][j])
            res.append(tmp[::-1])
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.rotateMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3))
