# -*- coding: utf-8 -*-
# @Time    : 2020/9/3 18:03
# @Author  : tmb

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


'''
「如果需要搜索整颗二叉树，那么递归函数就不要返回值，如果要搜索其中一条符合条件的路径，递归函数就需要返回值，因为遇到符合条件的路径了就要及时返回。」
'''


class Solution:
    # 递归
    def hasPathSum(self, root, sum: int) -> bool:
        if not root:
            return False
        if not root.left and not root.right:  # 遍历到叶子结点时，判断是否相等
            return sum == root.val
        # 这里存在回溯，把sum - root.val作为参数传进去，函数结束，sum的值没有改变
        # 遍历左子树和右子树，并减去当前值,左右子树一个成立即可
        return self.hasPathSum(root.left, sum - root.val) or self.hasPathSum(root.right, sum - root.val)


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


class Solution3:
    # 使用回溯
    flag = False

    def hasPathSum(self, root, _sum: int) -> bool:
        if not root:
            return False

        def dfs(root, path):
            if self.flag:  # 找到一个符合，就终止
                return
            if not root.left and not root.right:  # 叶子节点
                if path == _sum:
                    self.flag = True
            if root.left:
                # path += root.left.val
                dfs(root.left, path + root.left.val)
                # path -= root.left.val
            if root.right:
                # path += root.right.val
                dfs(root.right, path + root.right.val)
                # path -= root.right.val

        dfs(root, root.val)
        return self.flag


if __name__ == '__main__':
    head = TreeNode(1)
    head.left = TreeNode(2)
    a = Solution()
    print(a.hasPathSum(head, 1))
