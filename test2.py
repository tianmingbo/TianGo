class Solution:
    def maxsumofSubarray(self, arr):
        if len(arr) == 1:
            return arr[0]
        max_sum = 0
        res = 0
        for i in range(len(arr)):
            max_sum += arr[i]
            if max_sum < 0:
                max_sum = 0
            else:
                res = max(res, max_sum)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.maxsumofSubarray([1, -2, 3, 5, -2, 6, -1]))
