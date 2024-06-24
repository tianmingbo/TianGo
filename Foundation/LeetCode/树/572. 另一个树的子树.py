# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


'''
class Solution {
    public boolean isSubtree(TreeNode s, TreeNode t) {
        if(s==null||t==null){
            return false;
        }
        if(isSubtree(s.left,t)||isSubtree(s.right,t)||isSameTree(s,t)){
            return true;
        }
        return false;
    }
    boolean isSameTree(TreeNode p, TreeNode q) {
        if(p!=null&&q==null||p==null&&q!=null){
            return false;
        }
        if(p==null&&q==null){
            return true;
        }
        if(p.val!=q.val){
            return false; 
        }
        boolean a=isSameTree(p.left,q.left);
        boolean b=isSameTree(p.right,q.right);
        
        return a&&b;
    }
}
'''


class Solution:
    def isSubtree(self, s: TreeNode, t: TreeNode) -> bool:
        if not s or not t:
            return False

        def dfs(node1, node2):
            if not node1 and not node2:  # 如果两个子树的左右节点同时不存在
                return True
            if (not node1 and node2) or (node1 and not node2):  # 两个子树的左右节点有一个存在，另一个没有
                return False
            if node1.val != node2.val:  # 两个子树的值不同
                return False
            return dfs(node1.left, node2.left) and dfs(node1.right, node2.right)  # 中序遍历

        if self.isSubtree(s.left, t) or self.isSubtree(s.right, t) or dfs(s, t):  # 如果s的左右两边的子树有一个和t匹配上
            return True
        return False
