class Solution:
    def largestRectangleArea(self, heights) -> int:
        stack = [-1]
        max_res = 0
        for i in range(len(heights)):
            while len(stack) > 1 and heights[i] <= heights[stack[-1]]:
                max_res = max(max_res, heights[stack.pop()] * (i - stack[-1] - 1))
            stack.append(i)
        for i in range(len(stack) - 1):
            max_res = max(max_res, heights[stack.pop()] * (len(heights) - 1 - stack[-1]))
        return max_res


if __name__ == '__main__':
    a = Solution()
    print(a.largestRectangleArea([2, 1, 5, 6, 2, 3]))
