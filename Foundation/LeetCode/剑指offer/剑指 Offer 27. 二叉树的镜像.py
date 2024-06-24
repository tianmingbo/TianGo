
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def mirrorTree(self, root: TreeNode) -> TreeNode:
        '''实质是后序遍历'''
        if not root:
            return root
        left = self.mirrorTree(root.left)
        right = self.mirrorTree(root.right)
        root.left, root.right = right, left
        return root
