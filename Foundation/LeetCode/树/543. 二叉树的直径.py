# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        if not root:
            return 0
        self.res = 0

        def dfs(root):
            if not root:
                return 0
            l = dfs(root.left)  # 左子树的高度
            r = dfs(root.right)  # 右子树的高度
            self.res = max(self.res, l + r)  # 保存中间结果，可能不路过根
            return max(l, r) + 1  # 返回左右字树中最高的

        dfs(root)
        return self.res
