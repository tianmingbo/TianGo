from typing import List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        res = []
        queue = [root]
        while queue:
            layer = []
            layer_val=[]
            for _ in range(len(queue)):
                tmp = queue.pop(0)
                layer_val.append(tmp.val)
                if tmp.left:
                    layer.append(tmp.left)
                if tmp.right:
                    layer.append(tmp.right)
            queue = (layer[:])
            res.append(layer_val)
        return res