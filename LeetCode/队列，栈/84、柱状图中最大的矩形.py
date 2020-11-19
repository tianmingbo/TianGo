class Solution:
    def largestRectangleArea(self, heights) -> int:
        # if len(heights) == 0:
        #     return 0
        # if len(heights) == 1:
        #     return heights[0]
        # stack = [-1]
        # res = 0
        # for i in range(len(heights)):  # 栈，单调递增栈
        #     while len(stack) > 1 and heights[i] < heights[stack[-1]]:  # 如果下一列小于上一列，弹出，计算最大值
        #         res = max(res, heights[stack.pop()] * (i - stack[-1] - 1))
        #     stack.append(i)  # 下一列大于上一列，append
        #
        # for j in range(len(stack) - 1):  # 最后列表中的值的处理 [1,2,3]
        #     res = max(res, (len(heights) - stack[-1] - 1) * heights[stack.pop()])
        # return res

        heights.append(0)
        stack = [-1]
        ans = 0
        for i in range(len(heights)):
            while heights[i] < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = i - stack[-1] - 1
                ans = max(ans, h * w)
            stack.append(i)
        heights.pop()
        return ans

if __name__ == '__main__':
    a = Solution()
    print(a.largestRectangleArea([7,6,5,4,3,2,1]))
