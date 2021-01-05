# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if not root:
            return True

        def dfs(left, right):
            if not left and not right:
                return True
            if left and right and left.val == right.val:
                return dfs(left.left, right.right) and dfs(left.right, right.left)
            return False

        return dfs(root.left, root.right)
