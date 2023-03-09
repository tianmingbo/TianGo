# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 18:49
# @Author  : tmb
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        if not root:
            return "[]"
        res = []
        queue = [root]
        while queue:
            tmp = queue.pop(0)
            if tmp:
                res.append(tmp.val)
                queue.append(tmp.left)
                queue.append(tmp.right)
            else:
                res.append('null')
        return str(res)

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        root = TreeNode(data[0])
        i, n = 0, len(data) - 1
        while i <= n:
            pass

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.deserialize(codec.serialize(root))
