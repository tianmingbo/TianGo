class Solution:
    def lowestCommonAncestor(self, root, o1, o2):
        if not root:
            return
        if o1 == root.val:
            return o1
        if o2 == root.val:
            return o2
        left = self.lowestCommonAncestor(root.left, o1, o2)
        right = self.lowestCommonAncestor(root.right, o1, o2)
        if left and right:
            return root.val
        return left or right
