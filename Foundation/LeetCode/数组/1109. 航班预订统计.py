from typing import List


# 差分数组

class Solution:

    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        diff = [0] * n
        for fst, lst, val in bookings:
            diff[fst - 1] += val
            if lst < n:
                diff[lst] -= val
        from itertools import accumulate
        return list(accumulate(diff))


if __name__ == '__main__':
    a = Solution()
    print(a.corpFlightBookings(bookings=[[1, 2, 10], [2, 3, 20], [2, 5, 25]], n=5))
