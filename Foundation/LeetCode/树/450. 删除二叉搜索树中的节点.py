# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 17:17
# @Author  : tmb
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


'''
第一种情况：没找到删除的节点，遍历到空节点直接返回了
找到删除的节点

    第二种情况：左右孩子都为空（叶子节点），直接删除节点， 返回NULL为根节点
    第三种情况：删除节点的左孩子为空，右孩子不为空，删除节点，右孩子补位，返回右孩子为根节点
    第四种情况：删除节点的右孩子为空，左孩子不为空，删除节点，左孩子补位，返回左孩子为根节点
    第五种情况：左右孩子节点都不为空，则将删除节点的左子树头结点（左孩子）放到删除节点的右子树的最左面节点的左孩子上，返回删除节点右孩子为新的根节点
'''


class Solution:
    def deleteNode(self, root: TreeNode, key: int) -> TreeNode:
        if not root:
            return root

        if root.val == key:
            if root.right and root.right.left:  # 有右节点且右节点存在左节点
                tmp = root.right
                while tmp.left:  # 向左找到左节点
                    tmp = tmp.left
                root.val, tmp = tmp.val, self.deleteNode(root, tmp.val)  # 删除最左节点
                return root

            elif not root.right and root.left:  # 有左节点
                root = root.left
                return root

            elif not root.left and root.right:  # 有右节点
                root = root.right
                return root

            elif root.left and root.right:  # 有右节点和左节点，注意root左节点的处理
                root.right.left = root.left
                root = root.right
                return root

            elif not root.left and not root.right:  # 没有左节点和右节点
                root = None
                return root

        elif root.val > key:
            root.left = self.deleteNode(root.left, key)
        else:
            root.right = self.deleteNode(root.right, key)

        return root
