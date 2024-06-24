from typing import List
import collections


class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        if len(points) == 1:
            return 1

        ans, size = 0, len(points)
        # y = a * x + b
        x, y = collections.defaultdict(int), collections.defaultdict(int)
        for p in points:
            x[p[0]] += 1
            y[p[1]] += 1
            ans = max(ans, x[p[0]], y[p[1]])
        print(x,y,ans)

        ab = collections.defaultdict(set)
        for i in range(size):
            for j in range(i + 1, size):
                x1, y1 = points[i][0], points[i][1]
                x2, y2 = points[j][0], points[j][1]
                if x1 == x2 or y1 == y2:
                    # already calculated
                    continue
                a = (y1 - y2) / (x1 - x2)
                b = (x1 * y2 - x2 * y1) / (x1 - x2)
                ab[(a, b)].add(tuple(points[i]))
                ab[(a, b)].add(tuple(points[j]))
                ans = max(ans, len(ab[(a, b)]))

        return ans


if __name__ == '__main__':
    a = Solution()
    print(a.maxPoints([[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]))
