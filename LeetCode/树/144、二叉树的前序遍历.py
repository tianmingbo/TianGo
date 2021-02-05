# 同中序遍历

class Solution:
    def preorderTraversal(self, root):
        # 递归
        res = []
        res.append(root.val)
        self.preorderTraversal(root.left)
        self.preorderTraversal(root.right)
