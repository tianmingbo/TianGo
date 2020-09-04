# -*- coding: utf-8 -*-
# @Time    : 2020/9/3 18:03
# @Author  : tmb

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    # 递归
    def hasPathSum(self, root, sum: int) -> bool:
        if not root:
            return False
        if not root.left and not root.right:  # 遍历到叶子结点时，判断是否相等
            return sum == root.val
        return self.hasPathSum(root.left, sum - root.val) or self.hasPathSum(root.right,
                                                                             sum - root.val)  # 遍历左子树和右子树，并减去当前值,左右子树一个成立即可


class Solution2:
    # 层序遍历，广度优先
    def hasPathSum(self, root, sum: int) -> bool:
        if not root:
            return False
        import collections
        queue = collections.deque()  # 双端队列
        all_res = collections.deque()
        queue.append(root)
        all_res.append(root.val)
        while queue:
            tmp = queue.popleft()
            res = all_res.popleft()
            if not tmp.left and not tmp.right:  # 叶子结点
                if res == sum:
                    return True
            if tmp.left:
                queue.append(tmp.left)
                all_res.append(res + tmp.left.val)
            if tmp.right:
                queue.append(tmp.right)
                all_res.append(res + tmp.right.val)
        return False


if __name__ == '__main__':
    head = TreeNode(1)
    head.left = TreeNode(2)
    a = Solution()
    print(a.hasPathSum(head, 1))
