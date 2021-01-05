from typing import List


class Solution:
    def verifyPostorder(self, postorder: List[int]) -> bool:
        def helper(i, j):
            if i >= j:
                return True
            small = i
            while postorder[small] < postorder[j]:
                small += 1
            big = small
            while postorder[big] > postorder[j]:
                big += 1
            return big == j and helper(i, small - 1) and helper(small, j - 1)

        return helper(0, len(postorder) - 1)


'''
核心思想就是 从前往后找，先找到小于最后一个值的索引，再向后找到大于最后一个值的索引
递归查找，i>=j 退出
'''
if __name__ == '__main__':
    a = Solution()
    print(a.verifyPostorder([1, 3, 2, 6, 5]))
